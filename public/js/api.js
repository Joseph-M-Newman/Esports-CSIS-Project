class api {
    /**
     * Constructs api object
     *
     * @param	username
     * @param	password
     *
     * The username and password don't have to be for
     * a user that exists, they just have to be non null
     *
     * If the user does not exist, calling add_user() will
     * create an account for them
     */
    constructor(username, password) {
      this.username = username;
      this.password = password;
    }
  
    /**
     * Makes a get call to the api
     * Does not normally need to be used
     *
     * @return json with payload or err
     */
    async api_get(func, body) {
      let url = "/api/" + func;
      let query = "?";
  
      for (var v in body) {
        if (!body[v]) continue;
        query += v + "=" + body[v];
      }
  
      if (query.length > 1) url += query;
  
      let call = await fetch(url, {
        method: "GET",
        headers: { "Content-Type": "application/json" },
      });
      return await call.json();
    }
  
    /**
     * Makes a non get call to the api
     * Does not normally need to be used
     *
     * @return json with payload or err
     */
    async api_call(func, method, body) {
      let call = await fetch("/api/" + func, {
        method: method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
  
      return await call.json();
    }
  
    /**
     * Gets list of users
     *
     * @param	username	(optional)
     * @return	json of users or err
     */
    async get_users(username) {
      return this.api_get("user", username);
    }
  
    /**
     * Authenticates user that the api was created with
     *
     * @return json with either msg or err
     */
    async login() {
      return this.api_call("login", "POST", {
        username: this.username,
        password: this.password,
      });
    }
  
    /**
     * Creates user account
     *
     * @return json with either msg or err
     */
    async add_user() {
      return this.api_call("adduser", "POST", {
        username: this.username,
        password: this.password,
      });
    }
  
    async update_user(newusername, newpassword)
    {
        return this.api_call("updateuser", "PUT", {
          username: this.username,
          password: this.password,
          newusername: newusername,
          newpassword: newpassword
        });
    }
  
    /**
     * Deletes user account
     *
     * @return json with either msg or err
     */
    async delete_user() {
      return this.api_call("deleteuser", "POST", {
        username: this.username,
        password: this.password,
      });
    }


}
  