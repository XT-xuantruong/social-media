import { data } from "autoprefixer";
import ApiService from "./ApiService";

class PostServices extends ApiService {
  get entity() {
    return "posts";
  }
  async create(credential) {
    const { body } = credential;
    var data = {
      body: body,
    };
    console.log(data);
    return this.request({
      method: "post",
      url: `/${this.entity}/create/`,
      data: data,
    });
  }

  async getProfileFeed(id) {
    return this.request({
      method: "get",
      url: `/${this.entity}/profile/${id}/`,
    });
  }

  async getPostDetail(id) {
    return this.request({
      method: "get",
      url: `/${this.entity}/${id}/`,
    });
  }

  async createComent(credential, id) {
    var data = {
      body: credential,
    };
    return this.request({
      method: "post",
      url: `/${this.entity}/${id}/comment/`,
      data: data,
    });
  }
}

export default new PostServices();
