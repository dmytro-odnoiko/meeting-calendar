import { api } from 'boot/axios'

export const getEvents = async ({ commit, dispatch }, payload) => {
  let url = '/meetings?token=' + payload
  await api.get(url).then(response => {
      commit('setEvents', response.data)
    })
}

export const postEvent = async ({ commit, dispatch }, payload) => {
  let url = '/meetings?token=' + payload.token
  delete payload.token
  await api.post(url, payload).then(response => {
    })
}

export const putEvent = async ({ commit, dispatch }, payload) => {
  let url = '/meetings/' + payload.id + '?token=' + payload.token
  delete payload.token
  await api.put(url, payload).then(response => {
    })
}