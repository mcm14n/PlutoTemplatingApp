import axios from "axios";
import api from "./api";

export async function renderTemplate(template) {
  return axios.post(api.RENDER_TEMPLATE, { template });
}
