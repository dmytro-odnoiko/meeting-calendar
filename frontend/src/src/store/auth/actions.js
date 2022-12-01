import { api } from 'boot/axios'

export const doLogin = async ({ commit, dispatch }, payload) => {
  await api.post('/token/', 
      {'username':payload.username, 'password': payload.password},
      {
        headers: { 
              "Content-Type": "application/x-www-form-urlencoded"
        }
      }
    ).then(response => {
      const token = response.data.access_token
      commit('setToken', token)
  })
}

export const doSingUp = async ({ commit, dispatch }, payload) => {
  await api.post('/users/', payload).then(response => {
  })
}

export const signOut = ({ commit }) => {
  api.defaults.headers.common.Authorization = ''
  commit('removeToken')
}


export const init = async ({ commit, dispatch }) => {
  const token = localStorage.getItem('token')
  if (token) {
    await commit('setToken', JSON.parse(token))
    dispatch('getMe', JSON.parse(token))
  } else {
    commit('removeToken')
  }
}
