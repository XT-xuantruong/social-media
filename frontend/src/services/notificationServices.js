import ApiService from "./ApiService";
import { getConfigApp } from "./appConfig";
import { useUserStore } from "@/stores/user";

class NotificationServices extends ApiService {
  get entity() {
    return "notifications";
  }

  async setRead(notification) {
    const option = {
      method: "post",
      url: `/${this.entity}/read/${notification.id}/`,
    };
    return this.request(option);
  }
}

export default new NotificationServices();
