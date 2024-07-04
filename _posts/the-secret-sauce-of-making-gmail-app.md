---
layout: post
title:  "The secret sauce of making Gmail app"
date:   2024-07-04 10:49:52 +0700
categories: Making Chrome Extension
---
The Gmail app I am talking about here is the extended UI that load on openning Gmail website, like this one from Calendly: https://calendly.com/integration/calendly-for-chrome

The thing is: Gmail is very strict about what you can do with their UI. They have a lot of security measures to prevent you from doing anything that might harm their users. So, how bypass these measures and carry on doing what you want (or are required) to do anyway?

For example: I am trying to make an extension that use AntD design components and under the hood they use all kind of operations that require trusted policies like assigning innerHTML, create new Worker service and so on. Apparently Gmail won't allow you to do it easily. So what you have to do is OVERRIDING THE `Content Security Policy` of the first response from Gmail server when you open Gmail app, which is https://mail.google.com/mail/u/0/

The RECIPES:
- 
- 