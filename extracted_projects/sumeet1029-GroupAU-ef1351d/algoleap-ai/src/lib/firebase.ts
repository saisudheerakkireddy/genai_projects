import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

const firebaseConfig = {
  apiKey: "AIzaSyDHvqDRGqDMbn2IpqRhNUqKfxPwitdjT58",
  authDomain: "algoleap-ai.firebaseapp.com",
  projectId: "algoleap-ai",
  storageBucket: "algoleap-ai.appspot.com",
  messagingSenderId: "116579619151012992878",
  appId: "1:116579619151012992878:web:placeholder", // You'll need to get this from Firebase Console
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
