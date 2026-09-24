import { mount } from '@vue/test-utils'
import { describe, it, expect, vi } from 'vitest'
import ToyDatabase from '../ToyDatabase.vue'

describe('ToyDatabase.vue', () => {
  const library = { id: 1, name: 'Library A' }

  it('renders the component with library name', () => {
    const wrapper = mount(ToyDatabase, {
      props: { library }
    })
    expect(wrapper.text()).toContain('Toy Database')
    expect(wrapper.text()).toContain('Library A')
  })

  it('emits close event when close button is clicked', async () => {
    const wrapper = mount(ToyDatabase, {
      props: { library }
    })
    await wrapper.find('button').trigger('click')
    expect(wrapper.emitted()).toHaveProperty('close')
  })

  it('loads inventory and allows placing holds up to limit', async () => {
    vi.useFakeTimers()
    const wrapper = mount(ToyDatabase, {
      props: { library }
    })

    expect(wrapper.text()).toContain('Loading inventory...')

    // Fast-forward fetch timeout
    vi.runAllTimers()
    await wrapper.vm.$nextTick()

    // Assuming we have at least 4 toys in mock data
    const buttons = wrapper.findAll('button').filter(b => b.text() === 'Place Hold')
    expect(buttons.length).toBeGreaterThanOrEqual(4)

    // Place 3 holds
    await buttons[0].trigger('click')
    await buttons[1].trigger('click')
    await buttons[2].trigger('click')

    expect(wrapper.text()).toContain('Holds Placed: 3 / 3')

    // Try placing a 4th hold - it should be disabled or label should change
    // Since UI disables the button, we can't trigger click normally, but we can verify text changed
    const disabledButtons = wrapper.findAll('button').filter(b => b.text() === 'Hold Limit Reached')
    expect(disabledButtons.length).toBeGreaterThan(0)

    vi.useRealTimers()
  })
})
