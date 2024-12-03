---
layout: post
title: How to serve local, uncommited FE code on any stage or production domains
date: 2024-12-03 10:46:18 +0700
categories: []
---

Connecting local FE to stage / production server is a justified need, especially when:

- You need to inspect how the app behave with some specific data on production environment
- You don't want to start a local BE to save up device resources and booting time

A typical solution would be to use the local FE app to send request directly to server, but sometimes you just can not do it easily due to Authentication / CORS constraints.

In this post I will show you how to serve local FE code right on your stage domain without deploying nor adding any line of code to your codebase. It will also break no CORS policy and even support HMR.

If this sound too good to be true, take this video recording as a proof:

<iframe width="560" height="315" src="https://www.youtube.com/embed/7BCU-dzku8g?si=y7IeZqSFC-lN4Bia" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
P/s: the public demo is using webpack but the hot reload in my main private project is even snappier with Vite

# The solution in general

The main idea is to intercept and modify the HTML response of server so that it will return the local page instead of its hosted version. In the case of a ReactJs app, after doing this we would have the index.html response no longer load a script from a built [domain].com/index-[HASH].js file but rather the local index.js file that lead further requests to local dev server.

All the interception will happen at the browser layer with the help of a chrome extension. Yes, what you can do with chrome extension is pretty wild.

# How to get it done, step by step

## Prerequisite

- Your local setup has to be served on `https` or else the https live domain won't be able to fetch http request from your local due to security reason.

## Steps

- Start your local FE server
- Download this extension: https://chromewebstore.google.com/detail/modresponse-mock-and-repl/bbjcdpjihbfmkgikdkplcalfebgcjjpm
- Go to the website you want to override FE
- In DevTools Network panel, search for the first html document response and get its endpoint. The endpoint should be the GET method of the url you are trying to access and the response content should look like this:

```html
<!DOCTYPE html>
<html>
  <head>
    ...
    <meta content="width=device-width, initial-scale=1" name="viewport" />
  </head>
  <body>
    <div id="root"></div>
    <script type="module">
      window.appEnvironment = "content-stage"
      ...
    </script>
    <script
      src="https://s3.nemothecollector.dev/assets/application.jsx-23fa6ac5.js"
      crossorigin="anonymous"
      type="module"
    ></script>
    ...
  </body>
</html>
```

- Open the option page of Mod Response Chrome Extension. Click `Mod` button and choose `Replay Response` and input the endpoint above - This help you record everything about the specified endpoints you input: headers, body, etc..
- Rerun the stage webpage again for the request to be captured.
- Reload the option page, there should be a link that open the captured response in details. We will be changing its content in this modal (gonna name this modal MOD_MODAL for reuse)
- Open the dev server, depend on your infrastructure but the first time you do this you might need to start a local BE so that the whole local app can be run as usual. Look for the same similar of HTML document request on this app and copy its response. It should look like this:

```html
<!DOCTYPE html>
<html>
  <head>
    ...

    <meta content="width=device-width, initial-scale=1" name="viewport" />
  </head>
  <body>
    <div id="root"></div>
    <div id="modal"></div>
    <script type="module">
       window.appEnvironment = "development";
      ...
    </script>
    <script type="module">
      import RefreshRuntime from "https://localhost:3036/webapp-ui-kit/@react-refresh";

      RefreshRuntime.injectIntoGlobalHook(window);
      window.$RefreshReg$ = () => {};
      window.$RefreshSig$ = () => (type) => type;
      window.__vite_plugin_react_preamble_installed__ = true;
    </script>
    <script
      src="https://localhost:3036/app/react/main/application.jsx"
      crossorigin="anonymous"
      type="module"
    ></script>
  </body>
</html>
```

IMPORTANT NOTICE: Check if the content of local endpoint have relative path and update to absolute path (for example `index.js` to `https://localhost:3036/index.js`). If not, all relative paths will fall to the serving domains. This can be done manually or you can reconfig your bundler to auto-add the base to every file url.

- Copy the whole local response to the MOD_MODAL and hit save
- Reload stage webpage
- Try editting some code to see if it works (spoiler: it would work, finger crossed).

The first time it worked, I literally jumped. I hope it can help you avoid many boring day at work with blind pushes and waiting for the CI to complete.

Have fun programming, call me Phat Or Nemo.
