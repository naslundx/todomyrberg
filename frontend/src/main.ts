import "./assets/main.css";

import { createApp } from "vue";
import { createPinia } from "pinia";

import App from "./App.vue";
import router from "./router";

import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
import {
  faCheck,
  faClock,
  faPlus,
  faEdit,
  faTrash,
  faCog,
  faCheckCircle,
  faArrowLeft,
  faSignOutAlt,
  faRotateRight,
} from "@fortawesome/free-solid-svg-icons";

const app = createApp(App);

app.directive("visible", function (el, binding) {
  el.style.visibility = !!binding.value ? "visible" : "hidden";
});

app.use(createPinia());
app.use(router);
app.component("FontAwesomeIcon", FontAwesomeIcon);

library.add(
  faCheck,
  faClock,
  faPlus,
  faEdit,
  faTrash,
  faCog,
  faCheckCircle,
  faArrowLeft,
  faSignOutAlt,
  faRotateRight,
);

app.mount("#app");
