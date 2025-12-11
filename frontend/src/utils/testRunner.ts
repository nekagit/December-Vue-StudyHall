/**
 * Test runner utility for running Python code tests with Pyodide
 */

export interface TestCase {
  input: string
  output: string
}

export interface TestResult {
  passed: boolean
  expected: string
  actual: string
  testCase: TestCase
}

/**
 * Run tests against user code using Pyodide
 */
export async function runTests(
  pyodide: any,
  userCode: string,
  testCases: TestCase[]
): Promise<TestResult[]> {
  const results: TestResult[] = []

  try {
    // Execute the user's code first to define functions
    await pyodide.runPythonAsync(userCode)

    // Run each test case
    for (const testCase of testCases) {
      try {
        // Capture stdout
        let output = ''
        pyodide.setStdout({ batched: (msg: string) => {
          output += msg
        }})

        // Execute the test case and capture result
        const testCode = `
import json
import sys

# Execute the test case
try:
    result = ${testCase.input}
    # Convert result to JSON-like string representation
    if isinstance(result, bool):
        result_str = str(result)
    elif isinstance(result, (int, float)):
        result_str = str(result)
    elif isinstance(result, str):
        result_str = repr(result)  # Use repr to preserve quotes
    elif isinstance(result, (list, tuple)):
        result_str = str(result).replace("'", '"') if isinstance(result, tuple) else str(result)
    elif isinstance(result, dict):
        result_str = str(result)
    else:
        result_str = str(result)
    sys.stdout.write("RESULT:" + result_str + "\\n")
except Exception as e:
    sys.stdout.write("ERROR:" + str(e) + "\\n")
`

        await pyodide.runPythonAsync(testCode)

        // Extract result from output
        let actualStr = ''
        if (output.includes('RESULT:')) {
          actualStr = output.split('RESULT:')[1]?.split('\n')[0]?.trim() || ''
        } else if (output.includes('ERROR:')) {
          const errorMsg = output.split('ERROR:')[1]?.split('\n')[0]?.trim() || ''
          results.push({
            passed: false,
            expected: testCase.output,
            actual: `Error: ${errorMsg}`,
            testCase
          })
          continue
        } else {
          results.push({
            passed: false,
            expected: testCase.output,
            actual: 'No output produced',
            testCase
          })
          continue
        }

        const expectedStr = testCase.output.trim()

        // Normalize comparison - handle different representations
        const normalize = (str: string) => {
          // Remove extra quotes, normalize whitespace
          return str.replace(/^['"]|['"]$/g, '').replace(/\s+/g, ' ').trim()
        }

        const normalizedActual = normalize(actualStr)
        const normalizedExpected = normalize(expectedStr)

        // Compare: try exact match, normalized match, and whitespace-ignored match
        const passed = actualStr === expectedStr ||
                      normalizedActual === normalizedExpected ||
                      actualStr.replace(/\s/g, '') === expectedStr.replace(/\s/g, '') ||
                      JSON.stringify(actualStr) === JSON.stringify(expectedStr)

        results.push({
          passed,
          expected: expectedStr,
          actual: actualStr,
          testCase
        })
      } catch (e: any) {
        results.push({
          passed: false,
          expected: testCase.output,
          actual: `Error: ${e.message || String(e)}`,
          testCase
        })
      }
    }
  } catch (e: any) {
    // If code execution fails, mark all tests as failed
    testCases.forEach(testCase => {
      results.push({
        passed: false,
        expected: testCase.output,
        actual: `Code execution error: ${e.message || String(e)}`,
        testCase
      })
    })
  }

  return results
}

/**
 * Load Pyodide if not already loaded
 */
export async function loadPyodide(): Promise<any> {
  // @ts-ignore
  if (window.loadPyodide) {
    // @ts-ignore
    return await window.loadPyodide()
  } else {
    return new Promise((resolve, reject) => {
      const script = document.createElement('script')
      script.src = "https://cdn.jsdelivr.net/pyodide/v0.25.0/full/pyodide.js"
      script.onload = async () => {
        try {
          // @ts-ignore
          const pyodide = await window.loadPyodide()
          resolve(pyodide)
        } catch (e) {
          reject(e)
        }
      }
      script.onerror = reject
      document.head.appendChild(script)
    })
  }
}



