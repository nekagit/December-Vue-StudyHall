import { createApp, type Component } from 'vue'

export function mountIslands(components: Record<string, Component>) {
  document.querySelectorAll('[data-vue-component]').forEach(el => {
    const componentName = el.getAttribute('data-vue-component')
    if (componentName && components[componentName]) {
      const props = JSON.parse(el.getAttribute('data-props') || '{}')
      const app = createApp(components[componentName], props)
      app.mount(el)
      console.log(`Mounted ${componentName}`)
    }
  })
}











