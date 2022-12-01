
const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/IndexPage.vue') }
    ]
  },
  {
    name: 'LoginIn',
    path: '/login',
    component: () => import('pages/Login.vue')
  },
  {
    name: 'signUpUser',
    path: '/signup',
    component: () => import('pages/SignUp.vue')
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
