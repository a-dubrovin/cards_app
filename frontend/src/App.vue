<template>
  <div id="app">
    <h1>Cards App.</h1>
    <div id="auth">
      <template v-if="token">
        <h2>Hello {{username}}! <button v-on:click="logout">Logout</button></h2>
      </template>
      <template v-else>
        <h2>Authentication</h2>
        <table class="fields">
          <tr>
            <td>Username: </td>
            <td><input v-model="username" type="text" name="username" ></td>
          </tr>
          <tr>
            <td>Password: </td>
            <td><input v-model="password" type="password" name="password"></td>
          </tr>
        </table>
        <div>All fields required</div>
        <div v-if="user_errors" class="errors">
          <div v-bind:key="error" v-for="error in user_errors">{{error}}</div>
        </div>
        <div>
           <button v-on:click="authorize" style="margin-right: 10px;">Authorize</button>
           <button v-on:click="register">Register</button>
        </div>
      </template>
    </div>
    <template v-if="token">
      <div id="cards">
        <h2>Cards</h2>
        <div id="list">
          <table class="cards">
            <thead>
              <td>Series</td>
              <td>Number</td>
              <td>Is active</td>
              <td>Issue date</td>
              <td>Expiration date</td>
            </thead>
            <tr v-bind:key="card"  v-for="card in cards_list">
              <td>{{card.series}}</td>
              <td>{{card.number}}</td>
              <td>{{card.is_active}}</td>
              <td>{{card.start_date}}</td>
              <td>{{card.end_date}}</td>
            </tr>
          </table>
        </div>
        <div>
          <button v-on:click="get_cards_list">Update cards list</button>
        </div>
        <div id="create_cards">
          <h3>Create new cards</h3>
          <span v-if="cards_errors">
            <div v-bind:key="key" v-for="(error, key) in cards_errors" class="errors">
              {{key}}: {{error}}
            </div>
          </span>
          <table class="fields">
            <tr>
              <td>Series: </td>
              <td><input v-model="cards_series" v-on:input="get_series" type="number" name="series" max="9999"></td>
              <td></td>
            </tr>
            <tr>
              <td>Cards Quantity: </td>
              <td><input v-model="cards_quantity" type="number" name="cards_quantity" v-bind:max="cards_available_count ? cards_available_count : 999999"></td>
              <td>
                <span v-if="cards_available_count">
                  Max: {{cards_available_count}}
                </span>
              </td>
            </tr>
            <tr>
              <td>Cards validity: </td>
              <td>
                <select v-model="cards_validity">
                  <option v-for="option in cards_validity_options" v-bind:key="option" v-bind:value="option.value">
                    {{ option.text }}
                  </option>
                </select>
              </td>
              <td></td>
            </tr>
          </table>
          <div>
            <button v-on:click="create_cards">Create cards</button>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script>

const register_url = 'http://127.0.0.1:8000/api/v1/account/register/'
const authorize_url = 'http://127.0.0.1:8000/api/v1/account/token/'
const cards_list_url = 'http://127.0.0.1:8000/api/v1/cards/'
const series_url = 'http://127.0.0.1:8000/api/v1/series/'

export default {
  name: 'App',
  data() {
    return {
      username: 'testuser', // Default username value
      password: 'testuser', // Default password value
      token: false,

      user_errors: [],
      cards_errors: [],

      cards_list: {},

      cards_series: 0,
      cards_quantity: 0,
      cards_validity: 1,
      cards_validity_options: [
        { text: '1 month', value: 1 },
        { text: '6 months', value: 6 },
        { text: '1 year', value: 12 },
        { text: '3 years', value: 36 }
      ],
      cards_available_count: null
    }
  },
  components: {
  },
  methods: {
    checkUserFields: function (e) {
      this.user_errors = [];
      if (!this.username) {
        this.user_errors.push('Username required.');
      }
      if (!this.password) {
        this.user_errors.push('Password required.');
      }
      e.preventDefault();
      if (this.user_errors.length > 0) {
        return false
      }
      else {
        return true
      }
    },
    authorize: function (e) {
      let is_valid = this.checkUserFields(e)

      if (is_valid) {
        this.$http.post(authorize_url, {
          username: this.username,
          password: this.password
        }, {
          emulateJSON: true
        }).then(response => {
          this.token = response.data['token'];
          this.password = ''
          this.get_cards_list()
        }).catch((error) => {
          this.user_errors = error.response.data;
        });
      }
    },
    register: function (e) {
      let is_valid = this.checkUserFields(e)

      if (is_valid) {
        this.$http.post(register_url, {
          username: this.username,
          password: this.password
        }, {
          emulateJSON: true
        }).then(response => {
          this.username = response.data['username'];
          this.authorize(e)
        }).catch((error) => {
          this.user_errors = error.response.data;
        });
      }
    },
    logout: function () {
      this.token = false;
    },
    get_cards_list: function () {
      if (this.token) {
        this.$http.get(cards_list_url, {
          emulateJSON: true,
          headers: {
            Authorization: 'Token ' + this.token
          }
        }).then(response => {
          this.cards_list = response.data;
        });
      }
    },
    get_series: function () {
      if (this.token) {
        this.$http.get(series_url + this.cards_series + '/', {
          emulateJSON: true,
          headers: {
            Authorization: 'Token ' + this.token
          }
        }).then(response => {
          this.cards_available_count = response.data['available_numbers_count'];
        }).catch(() => {
          this.cards_available_count = null
        });
      }
    },
    create_cards: function () {
      this.cards_errors = []
      if (this.token) {
        this.$http.post(cards_list_url, {
          series: this.cards_series,
          cards_quantity: this.cards_quantity,
          validity: this.cards_validity
        }, {
          emulateJSON: true,
          headers: {
            Authorization: 'Token ' + this.token
          }
        }).then(() => {
          this.get_cards_list()
        }).catch((error) => {
          this.cards_errors = error.response.data;
        });
      }
    }
  }
}
</script>

<style>
div {
  margin: 5px 0px;
}
.fields {
  margin: auto;
  padding: 0px;
}
.fields td {
  margin: 3px 5px;
  text-align: left;
}
.fields li input, select {
  width: 150px;
}
.cards {
  margin: auto;
}
.cards thead {
  font-weight: bold;
  background-color: darkgray;
}
.cards td {
  padding: 3px 5px;
}

.errors {
  color: red;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  background-color: antiquewhite;
  width: 500px;
  margin: 20px auto;
  padding: 20px;
}
</style>
