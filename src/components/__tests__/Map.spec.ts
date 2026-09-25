import { mount } from '@vue/test-utils'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import Map from '../Map.vue'
import L from 'leaflet'

// Mock leaflet as it requires a real DOM
vi.mock('leaflet', () => {
  const markerMock = {
    addTo: vi.fn().mockReturnThis(),
    bindPopup: vi.fn().mockReturnThis(),
    on: vi.fn().mockReturnThis()
  }
  const L = {
    map: vi.fn(() => ({
      setView: vi.fn().mockReturnThis(),
      remove: vi.fn()
    })),
    tileLayer: vi.fn(() => ({
      addTo: vi.fn()
    })),
    marker: vi.fn(() => markerMock),
    icon: vi.fn()
  }
  return { default: L }
})

describe('Map.vue', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    global.fetch = vi.fn()
  })

  it('renders the map container', () => {
    const wrapper = mount(Map)
    expect(wrapper.find('#map-container').exists()).toBe(true)
  })

  it('displays library and community center markers', async () => {
    const wrapper = mount(Map)
    
    await new Promise(resolve => setTimeout(resolve, 0))
    
    // 3 library markers + 15 community center markers = 18
    expect(L.marker).toHaveBeenCalledTimes(18)
    
    // Check one of the hardcoded community centers
    expect(L.marker).toHaveBeenCalledWith([44.9602, -93.2536], expect.any(Object))
  })
})
