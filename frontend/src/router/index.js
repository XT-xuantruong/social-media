import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import SignupView from "@/views/SignupView.vue";
import LoginView from "@/views/LoginView.vue";
import FeedView from "@/views/FeedView.vue";
import MessagesView from "@/views/MessagesView.vue";
import SearchView from "@/views/SearchView.vue";
import ProfileView from "@/views/ProfileView.vue";
import FriendsView from "@/views/FriendsView.vue";
import PostView from "@/views/PostView.vue";
import EditProfileView from "@/views/EditProfileView.vue";
import TrendView from "@/views/TrendView.vue";
<<<<<<< HEAD
import EditPasswordView from '../views/EditPasswordView.vue'

=======
>>>>>>> 4bddc1161a5398f5e73e8e4faa0df77adf537c53
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/feed",
      name: "feed",
      component: FeedView,
    },
    {
      path: "/signup",
      name: "signup",
      component: SignupView,
    },
    {
      path: "/login",
      name: "login",
      component: LoginView,
    },
    {
      path: "/messages",
      name: "messages",
      component: MessagesView,
    },
    {
      path: "/search",
      name: "search",
      component: SearchView,
    },
    {
      path: "/profile/:id",
      name: "profile",
      component: ProfileView,
    },
    {
      path: "/profile/edit",
      name: "editprofile",
      component: EditProfileView,
    },
    {
      path: "/profile/:id/friends",
      name: "friends",
      component: FriendsView,
    },
    {
      path: "/:id",
      name: "postview",
      component: PostView,
    },
    {
      path: "/about",
      name: "about",
      component: () => import("../views/AboutView.vue"),
    },
    {
      path: "/trends/:id",
      name: "trendview",
      component: TrendView,
    },
    {
      path: '/profile/edit/password',
      name: 'editpassword',
      component: EditPasswordView
    },
  ],
});

export default router;
