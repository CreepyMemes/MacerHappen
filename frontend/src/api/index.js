import axiosInstance from './axios/interceptors';
import * as auth from './services/auth';
import * as organizer from './services/organizer';
import * as participant from './services/participant';
import * as pub from './services/public';
import * as image from './services/image';

const api = {
  instance: axiosInstance,
  auth,
  organizer,
  participant,
  pub,
  image,
};

export default api;
