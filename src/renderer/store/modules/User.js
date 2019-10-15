const state = {
  user: {}
}

const mutations = {
  SET_USER (state, user) {
    state.user = user
  }
}

const actions = {
  set_user ({ commit }, user) {
    commit('SET_USER', user)
  }
}

export default {
  state,
  mutations,
  actions
}
