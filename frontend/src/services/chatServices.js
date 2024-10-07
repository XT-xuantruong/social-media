import ApiService from "./ApiService";

class ChatServices extends ApiService {
  get entity() {
    return "chat";
  }
  async getChat(pk) {
    return this.request({
      method: "get",
      url: `/${this.entity}/${pk}/get-or-create/`,
    });
  }

  async sendMessages(pk, body) {
    const data = {
      body: body,
    };
    return this.request({
      method: "post",
      url: `/${this.entity}/${pk}/send/`,
      data: data,
    });
  }
}

export default new ChatServices();
