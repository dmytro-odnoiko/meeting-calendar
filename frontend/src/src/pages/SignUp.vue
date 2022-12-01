<template>
    <div class="row" style="height: 90vh">
      <div v-bind:class="{'justify-center': $q.screen.md || $q.screen.sm ||$q.screen.xs}"
           class="col-12 col-md-6 flex absolute-center content-center">
        <q-card v-bind:style="$q.screen.lt.sm ? {'width': '80%'} : {'width': '50%'}"
                class="absolute-center content-center"
        >
          <q-card-section>
            <q-avatar size="103px" class="absolute-center shadow-10">
              <img src="~assets/avatar.svg" alt="avatar">
            </q-avatar>
          </q-card-section>
          <q-card-section>
            <div class="q-pt-lg">
              <div class="col text-h6 ellipsis flex justify-center">
                <h5 class="text-h5 text-uppercase q-my-none text-weight-regular">SignUp</h5>
              </div>
            </div>
          </q-card-section>
          <q-card-section>
            <q-form class="q-gutter-md" @submit.prevent="submitForm">
              <q-input label="Username" v-model="signup.email">
              </q-input>
              <q-input label="Password" type="password" v-model="signup.password">
              </q-input>
              <div>
                <q-btn class="full-width" color="primary" label="Register" type="submit" rounded></q-btn>
              </div>
            </q-form>
          </q-card-section>
        </q-card>
      </div>
    </div>
  </template>
  
<script>
  import { useQuasar } from 'quasar'
  import { mapActions } from 'vuex'
  
  let $q
  
  export default {
    name: 'signUp',
    data () {
      return {
        signup: {
          email: '',
          password: ''
        }
      }
    },
    methods: {
      ...mapActions('auth', ['doSignUp']),
      async submitForm () {
        if (!this.signup.email || !this.signup.password) {
          $q.notify({
            type: 'negative',
            message: 'The entered data is invalid.'
          })
        } else if (this.signup.password.length < 6) {
          $q.notify({
            type: 'negative',
            message: 'Password must be 6 or more characters long.'
          })
        } else {
          try {
            await this.doSingUp(this.signup)
            const toPath = this.$route.query.to || '/login'
            this.$router.push(toPath)
          } catch (err) {
            console.log(err)
            if (err.response.data.detail) {
              $q.notify({
                type: 'negative',
                message: err.response.data.detail
              })
            }
          }
        }
      }
    },
    mounted () {
      $q = useQuasar()
    }
  }
  </script>
  
  <style scoped>
  .wave {
    position: fixed;
    height: 100%;
    left: 0;
    bottom: 0;
    z-index: -1;
  }
  </style>
  