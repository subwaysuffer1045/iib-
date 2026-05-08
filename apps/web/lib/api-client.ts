export const apiClient = {
  getInternships: async (params: any): Promise<{ data: any[], meta: any }> => {
    return { data: [], meta: { cursor: null, total: 0 } }
  },
  saveInternship: async (id: string) => {
    return { success: true }
  },
  unsaveInternship: async (id: string) => {
    return { success: true }
  }
}
