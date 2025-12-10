import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import HelloWorld from '@/components/HelloWorld.vue'

describe('HelloWorld', () => {
  it('renders props.msg when passed', () => {
    const msg = 'Hello World'
    const wrapper = mount(HelloWorld, { props: { msg } })
    expect(wrapper.text()).toContain(msg)
  })

  it('increments count when button is clicked', async () => {
    const wrapper = mount(HelloWorld, { props: { msg: 'Test' } })
    const button = wrapper.find('button')
    
    expect(button.text()).toContain('count is 0')
    
    await button.trigger('click')
    
    expect(button.text()).toContain('count is 1')
  })
})
