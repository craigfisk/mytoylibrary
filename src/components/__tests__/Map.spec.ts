import { mount } from '@vue/test-utils'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import Map from '../Map.vue'
import L from 'leaflet'

// Mock leaflet as it requires a real DOM
vi.mock('leaflet', () => {
  const markerMock = {
    addTo: vi.fn().mockReturnThis(),
    bindPopup: vi.fn().mockReturnThis()
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

  it('fetches community centers and displays them', async () => {
    const mockCenters = {
      elements: [
        { id: 101, tags: { name: 'Test Community Center' }, lat: 44.9, lon: -93.2 },
        { id: 102, tags: { name: 'Another Center' }, lat: 44.8, lon: -93.1 }
      ]
    }

    ;(global.fetch as any).mockResolvedValue({
      ok: true,
      json: vi.fn().mockResolvedValue(mockCenters)
    })

    const wrapper = mount(Map)
    
    // Wait for promises (fetch API) to resolve
    await new Promise(resolve => setTimeout(resolve, 0))

    expect(global.fetch).toHaveBeenCalled()
    
    // 3 library markers + 2 community center markers = 5
    expect(L.marker).toHaveBeenCalledTimes(5)
    
    // Ensure the specific coordinates were called
    expect(L.marker).toHaveBeenCalledWith([44.9, -93.2], expect.any(Object))
    expect(L.marker).toHaveBeenCalledWith([44.8, -93.1], expect.any(Object))
  })

  it('uses fallback community centers if fetch fails', async () => {
    ;(global.fetch as any).mockRejectedValue(new Error('Network Error'))

    const wrapper = mount(Map)
    await new Promise(resolve => setTimeout(resolve, 0))

    // 3 library markers + 3 fallback community center markers = 6
    expect(L.marker).toHaveBeenCalledTimes(6)
  })
})
