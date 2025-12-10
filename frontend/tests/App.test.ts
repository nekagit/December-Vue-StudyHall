import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { createRouter, createWebHistory } from 'vue-router'
import App from '@/App.vue'

// Mock fetch
global.fetch = vi.fn()

describe('App', () => {
  let router: any

  beforeEach(() => {
    router = createRouter({
      history: createWebHistory(),
      routes: [
        { path: '/', component: { template: '<div>Home</div>' } },
        { path: '/login', component: { template: '<div>Login</div>' } },
      ],
    })
    vi.clearAllMocks()
  })

  it('renders navigation', () => {
    const wrapper = mount(App, {
      global: {
        plugins: [router],
      },
    })

    expect(wrapper.find('nav').exists()).toBe(true)
    expect(wrapper.text()).toContain('StudyHall')
  })

  it('shows login link when not authenticated', () => {
    const mockFetch = vi.fn().mockResolvedValue({
      ok: false,
    })
    global.fetch = mockFetch

    const wrapper = mount(App, {
      global: {
        plugins: [router],
      },
    })

    expect(wrapper.text()).toContain('Login')
    expect(wrapper.text()).toContain('Register')
  })
})
