import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { createRouter, createWebHistory } from 'vue-router'
import Login from '@/views/Login.vue'

// Mock fetch
global.fetch = vi.fn()

describe('Login', () => {
  let router: any

  beforeEach(() => {
    router = createRouter({
      history: createWebHistory(),
      routes: [
        { path: '/login', component: Login },
        { path: '/', component: { template: '<div>Home</div>' } },
      ],
    })
    vi.clearAllMocks()
  })

  it('renders login form', () => {
    const wrapper = mount(Login, {
      global: {
        plugins: [router],
      },
    })

    expect(wrapper.find('input[type="email"]').exists()).toBe(true)
    expect(wrapper.find('input[type="password"]').exists()).toBe(true)
    expect(wrapper.find('button[type="submit"]').exists()).toBe(true)
  })

  it('shows error message on failed login', async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      ok: false,
      json: async () => ({ error: 'Invalid credentials' }),
    })
    global.fetch = mockFetch

    const wrapper = mount(Login, {
      global: {
        plugins: [router],
      },
    })

    await wrapper.find('input[type="email"]').setValue('test@example.com')
    await wrapper.find('input[type="password"]').setValue('wrongpassword')
    await wrapper.find('form').trigger('submit')

    await wrapper.vm.$nextTick()

    expect(wrapper.text()).toContain('Invalid credentials')
  })

  it('disables submit button while loading', async () => {
    const mockFetch = vi.fn().mockImplementation(
      () =>
        new Promise((resolve) => {
          setTimeout(() => {
            resolve({
              ok: true,
              json: async () => ({ success: true }),
            })
          }, 100)
        })
    )
    global.fetch = mockFetch

    const wrapper = mount(Login, {
      global: {
        plugins: [router],
      },
    })

    await wrapper.find('input[type="email"]').setValue('test@example.com')
    await wrapper.find('input[type="password"]').setValue('password')
    await wrapper.find('form').trigger('submit')

    await wrapper.vm.$nextTick()

    const button = wrapper.find('button[type="submit"]')
    expect(button.attributes('disabled')).toBeDefined()
    expect(button.text()).toContain('Signing in')
  })
})
