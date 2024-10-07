import axios from "axios";
import { useUserStore } from '@/stores/user'


const APP_API_URL = "http://localhost:8000/api/";
// const Cookie = require("js-cookie");
export default class Http {
  constructor(status) {
    this.handlerEnabled =
      status && status.handlerEnabled ? status.handlerEnabled : false;
    this.instance = axios.create({
      baseURL: APP_API_URL,
    });
    return this.init();
  }

  requestHandler(request) {
    const state = useUserStore();
    const { access  } = state.user;
    if (access && access.length !== 0) {
      request.headers["Authorization"] = `Bearer ${access}`;
    }
    return request;
  }

  errorHandler(error) {
    if (error?.response?.status === 401) {
      this.renewToken();
    }
    return Promise.reject(error);
  }

  successHandler(response) {
    if (this.handlerEnabled) {
      return response; 
    }
    return response;
  }

  init() {
    this.instance.interceptors.request.use((request) =>
      this.requestHandler(request)
    );
    this.instance.interceptors.response.use(
      (response) => this.successHandler(response),
      (error) => this.errorHandler(error)
    );
    return this.instance;
  }

  renewToken() {
    const state = useUserStore();
    const { refresh } = state.user;
    if (refresh) {
      state.refreshToken;
    }
    return false;
  }
}