import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import store from "../store/store";

const routes: Array<RouteRecordRaw> = [
    {
        path: "/",
        name: "home",
        component: () => import("../views/HomeView.vue"),
        // meta: {
        //   requiresAuth: false,
        //   requiresOperator: false
        // }
    },
    {
        path: "/login",
        name: "login",
        component: () => import("../views/LoginView.vue"),
        meta: {
          requiresAuth: false,
          requiresOperator: false
        }
    },
    {
        path: "/registry",
        name: "registry",
        component: () => import("../views/RegistryView.vue"),
        meta: {
          requiresAuth: false,
          requiresOperator: false
        }
    },
    {
        path: "/publish",
        name: "publish",
        component: () => import("../views/PublishView.vue"),
        meta: {
          requiresAuth: true,
          requiresOperator: false
        }
    },
    {
        path: "/rentals",
        name: "rentals",
        component: () => import("../views/RentalInfoView.vue"),
        meta: {
          requiresAuth: false,
          requiresOperator: false
        }
    },
    {
        path: "/log",
        name: "log",
        component: () => import("../views/LogView.vue"),
        meta: {
          requiresAuth: true,
          requiresOperator: true
        }
    },
    {
        path: "/mng",
        name: "mng",
        component: () => import("../views/ManageView.vue"),
        meta: {
          requiresAuth: true,
          requiresOperator: true
        }
    },
    // {
    //     path: "/test",
    //     name: "test",
    //     component: () => import("../views/TestView.vue"),
    //     meta: {
    //       requiresAuth: true,
    //       requiresOperator: true
    //     }
    // },
    {
        path: "/profile",
        name: "profile",
        component: () => import("../views/ProfileView.vue"),
        meta: {
          requiresAuth: true,
          requiresOperator: false
        }
    },
    {
        path: "/404",
        name: "404",
        component: () => import("../views/404NotFoundView.vue")
    }
]

// const routerHistory = createWebHistory()

const routers = createRouter({
    history:  createWebHistory('/'),
    routes: routes
})

const isLoggedIn = ():boolean => store.getters.isUserLoggedIn
const isOperator = ():boolean => store.getters.isOperator

routers.beforeEach((to, from, next) => {
 // ?? isLoggedIn and isOperator must be used as function to refresh the boolean value ??
  if (to.meta.requiresAuth && !isLoggedIn()) {
    // if not logged in, redirect to login page
    next({ name: 'login' });
  } else if (to.meta.requiresOperator && !isOperator()) {
    // if user is not operator, redirect to 404 page
      console.log(isOperator)
    next({ name: '404' });
  } else {
    next();
  }
})

export default routers