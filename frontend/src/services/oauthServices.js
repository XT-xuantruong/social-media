import ApiService from "./ApiService";
import { getConfigApp } from "./appConfig";
import { useUserStore } from "@/stores/user";

class OauthServices extends ApiService {
  get entity() {
    return "account";
  }

  async login(credential) {
    const { email, password } = credential;
    var data = {
      email: email,
      password: password,
    };
    console.log(data);
    return this.request({
      method: "post",
      url: `/${this.entity}/login/`,
      data: data,
    });
  }
  async signup(credential) {
    const { name, email, password1, password2 } = credential;
    var data = {
      name: name,
      email: email,
      password1: password1,
      password2: password2,
    };
    console.log(data);
    return this.request({
      method: "post",
      url: `/${this.entity}/signup/`,
      data: data,
    });
  }

  async logout() {
    const state = useUserStore();
    const data = {
      refresh: state.user.refresh,
    };
    const option = {
      method: "post",
      url: `/${this.entity}/blacklist/`,
      data: data,
    };
    return this.request(option);
  }

  async getme(access) {
    const option = {
      method: "get",
      url: `/${this.entity}/me/`,
      headers: {
        Authorization: `Bearer ${access}`,
      },
    };
    return this.request(option);
  }

  async sendFriendshipRequest(id) {
    return this.request({
      method: "post",
      url: `/${this.entity}/friends/${id}/request/`,
    });
  }

  async handleFriendshipRequest(status, pk) {
    return this.request({
      method: "post",
      url: `/${this.entity}/friends/${pk}/${status}/`,
    });
  }
  async getFriendshipRequest(pk) {
    return this.request({
      method: "get",
      url: `/${this.entity}/friends/${pk}/`,
    });
  }

  async getFriendSuggest() {
    return this.request({
      method: "get",
      url: `/${this.entity}/friends/suggested/`,
    });
  }

  async updateProfile(data) {
    console.log("data update", data);

    return this.request({
      method: "post",
      url: `/${this.entity}/editprofile/`,
      data: data,
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
  }

  async changePassword(formdata) {
    return this.request({
      method: "post",
      url: `/${this.entity}/editpassword/`,
      data: formdata,
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
  }

}

export default new OauthServices();
