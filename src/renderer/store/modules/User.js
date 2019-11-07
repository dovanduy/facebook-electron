import router from '../../router'
const state = {
  user: {}
}

const mutations = {
  SET_USER(state, user) {
    state.user = user
  },
  CLEAN_USER(state, user) {
    state.user = null
    router.push('/register')
  }
}

const actions = {
  set_user({ commit }, user) {
    commit('SET_USER', user)
  }
}

export default {
  state,
  mutations,
  actions
}
