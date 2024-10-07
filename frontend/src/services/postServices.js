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

  async get(id){
    return this.request({
      method: "get",
      url: `/${this.entity}/profile/${id}/`,
    });
  }
  
}

export default new PostServices();
