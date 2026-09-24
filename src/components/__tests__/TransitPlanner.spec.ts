import { mount } from '@vue/test-utils'
import { describe, it, expect, vi } from 'vitest'
import TransitPlanner from '../TransitPlanner.vue'

describe('TransitPlanner.vue', () => {
  const destinations = [
    { id: 1, name: 'Library A' },
    { id: 2, name: 'Library B' }
  ]

  it('renders the component correctly', () => {
    const wrapper = mount(TransitPlanner, {
      props: {
        destinations
      }
    })
    expect(wrapper.text()).toContain('Transit Planner')
    expect(wrapper.text()).toContain('Origin')
    expect(wrapper.text()).toContain('Destination')
  })

  it('emits close event when close button is clicked', async () => {
    const wrapper = mount(TransitPlanner, {
      props: {
        destinations
      }
    })
    await wrapper.find('button').trigger('click')
    expect(wrapper.emitted()).toHaveProperty('close')
  })

  it('displays mock routing results when Find Routes is clicked', async () => {
    vi.useFakeTimers()
    const wrapper = mount(TransitPlanner, {
      props: {
        destinations
      }
    })
    
    await wrapper.findAll('button').filter(b => b.text() === 'Find Routes')[0].trigger('click')
    
    // Fast-forward timeout
    vi.runAllTimers()
    await wrapper.vm.$nextTick()
    
    expect(wrapper.text()).toContain('Outbound Route')
    expect(wrapper.text()).toContain('Return Route')
    
    vi.useRealTimers()
  })
})
