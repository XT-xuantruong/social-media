import { data } from "autoprefixer";
import ApiService from "./ApiService";

class PostServices extends ApiService {
  get entity() {
    return "posts";
  }
  async create(data) {
    console.log("API log", data);
    return this.request({
      method: "post",
      url: `/${this.entity}/create/`,
      data: data,
      headers: {
        "Content-Type": "multipart/form-data",
      },
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

  async getTrends() {
    return this.request({
      method: "get",
      url: `/${this.entity}/trends/`,
    });
  }

  async getTrend(id) {
    return this.request({
      method: "get",
      url: `/${this.entity}/?trend=${id}/`,
    });
  }
}

export default new PostServices();
