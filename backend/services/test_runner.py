"""Service to run tests and collect results."""
import subprocess
import json
import os
import re
from pathlib import Path
from typing import Dict, Any

def run_backend_tests() -> Dict[str, Any]:
    """Run backend tests and return results."""
    backend_dir = Path(__file__).parent.parent
    original_dir = os.getcwd()
    
    try:
        os.chdir(backend_dir)
        
        # Run pytest and parse output
        result = subprocess.run(
            ["pytest", "-v", "--tb=short"],
            capture_output=True,
            text=True,
            timeout=300,
            check=False
        )
        
        # Parse pytest output to extract test results
        stdout_lines = result.stdout.split('\n')
        passed = 0
        failed = 0
        skipped = 0
        total = 0
        tests = []
        
        for line in stdout_lines:
            if ' PASSED' in line:
                passed += 1
                total += 1
                test_name = line.split(' PASSED')[0].strip()
                tests.append({"nodeid": test_name, "outcome": "passed"})
            elif ' FAILED' in line:
                failed += 1
                total += 1
                test_name = line.split(' FAILED')[0].strip()
                tests.append({"nodeid": test_name, "outcome": "failed"})
            elif ' SKIPPED' in line:
                skipped += 1
                total += 1
                test_name = line.split(' SKIPPED')[0].strip()
                tests.append({"nodeid": test_name, "outcome": "skipped"})
        
        report_data = {
            "summary": {
                "total": total,
                "passed": passed,
                "failed": failed,
                "skipped": skipped,
            },
            "tests": tests
        }
        
        return {
            "success": result.returncode == 0,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "report": report_data
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": "Tests timed out after 5 minutes"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
    finally:
        os.chdir(original_dir)

def get_backend_coverage() -> Dict[str, Any]:
    """Get backend coverage data."""
    backend_dir = Path(__file__).parent.parent
    coverage_file = backend_dir / "coverage.json"
    
    if not coverage_file.exists():
        return {
            "available": False,
            "message": "Coverage data not available. Run tests with coverage first."
        }
    
    try:
        with open(coverage_file, "r") as f:
            coverage_data = json.load(f)
        
        # Calculate summary
        files = coverage_data.get("files", {})
        total_lines = 0
        covered_lines = 0
        
        for file_data in files.values():
            summary = file_data.get("summary", {})
            total_lines += summary.get("num_statements", 0)
            covered_lines += summary.get("covered_lines", 0)
        
        coverage_percent = (covered_lines / total_lines * 100) if total_lines > 0 else 0
        
        return {
            "available": True,
            "coverage_percent": round(coverage_percent, 2),
            "total_lines": total_lines,
            "covered_lines": covered_lines,
            "files": {
                path: {
                    "coverage_percent": round(file_data.get("summary", {}).get("percent_covered", 0), 2),
                    "total_lines": file_data.get("summary", {}).get("num_statements", 0),
                    "covered_lines": file_data.get("summary", {}).get("covered_lines", 0),
                }
                for path, file_data in files.items()
            }
        }
    except Exception as e:
        return {
            "available": False,
            "error": str(e)
        }

def run_frontend_tests() -> Dict[str, Any]:
    """Run frontend tests and return results."""
    frontend_dir = Path(__file__).parent.parent.parent / "frontend"
    original_dir = os.getcwd()
    
    try:
        os.chdir(frontend_dir)
        
        # Run vitest
        result = subprocess.run(
            ["npm", "run", "test", "--", "--run"],
            capture_output=True,
            text=True,
            timeout=300,
            check=False
        )
        
        # Parse vitest output
        import re
        stdout_lines = result.stdout.split('\n')
        passed = 0
        failed = 0
        skipped = 0
        total = 0
        test_results = []
        
        for line in stdout_lines:
            if 'PASS' in line and 'tests' in line.lower():
                # Extract numbers from lines like "✓ 3 passed"
                match = re.search(r'(\d+)\s+passed', line)
                if match:
                    passed = int(match.group(1))
                    total += passed
            elif 'FAIL' in line and 'tests' in line.lower():
                match = re.search(r'(\d+)\s+failed', line)
                if match:
                    failed = int(match.group(1))
                    total += failed
            elif line.strip().startswith('✓') or line.strip().startswith('×'):
                # Test result line
                test_name = line.strip()
                if '✓' in test_name:
                    passed += 1
                    total += 1
                elif '×' in test_name:
                    failed += 1
                    total += 1
        
        report_data = {
            "numTotalTests": total,
            "numPassedTests": passed,
            "numFailedTests": failed,
            "numSkippedTests": skipped,
            "testResults": test_results
        }
        
        return {
            "success": result.returncode == 0,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "report": report_data
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": "Tests timed out after 5 minutes"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
    finally:
        os.chdir(original_dir)
    finally:
        os.chdir(original_dir)

def get_frontend_coverage() -> Dict[str, Any]:
    """Get frontend coverage data."""
    frontend_dir = Path(__file__).parent.parent.parent / "frontend"
    coverage_file = frontend_dir / "coverage" / "coverage-summary.json"
    
    if not coverage_file.exists():
        return {
            "available": False,
            "message": "Coverage data not available. Run tests with coverage first."
        }
    
    try:
        with open(coverage_file, "r", encoding="utf-8") as f:
            coverage_data = json.load(f)
        
        total = coverage_data.get("total", {})
        coverage_percent = total.get("lines", {}).get("pct", 0)
        
        return {
            "available": True,
            "coverage_percent": round(coverage_percent, 2),
            "total_lines": total.get("lines", {}).get("total", 0),
            "covered_lines": total.get("lines", {}).get("covered", 0),
            "files": {
                path: {
                    "coverage_percent": round(file_data.get("lines", {}).get("pct", 0), 2),
                    "total_lines": file_data.get("lines", {}).get("total", 0),
                    "covered_lines": file_data.get("lines", {}).get("covered", 0),
                }
                for path, file_data in coverage_data.items()
                if path != "total"
            }
        }
    except Exception as e:
        return {
            "available": False,
            "error": str(e)
        }
