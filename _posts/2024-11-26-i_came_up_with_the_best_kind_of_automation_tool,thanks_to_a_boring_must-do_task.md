---
layout: post
title: I came up with the best kind of automation tool,thanks to a boring must-do task
date: 2024-11-26 11:48:02 +0700
categories: []
---

# When you have a son who works IT

The back story is that about 1 month ago, the government decided to ditch most of the traditional paper work and instruct citizens to do these things online. This affect my father's business, which is motorbike retailing, in a good way because now our customers or his employee (FYI he has only one employee so the store's operation kinda halted when the guy went for such errand) do not have to spend half a day in public office to register a motorbike everytime one is sold. All the submission now happen in the dichvucong.gov.vn and IF THINGS GO SMOOTHLY (notice this part because it affect character development at the other half of the story) it will only take about 5 minutes for each case. Stonk.

But the problem is: not everyone, actually little percent of people is tech-literated enough to do these thing themselves. So my father recruited one more employee for this job, he has to know IT, live in this small town and cheap hiring cost so he can keep a competitive retailing price. After a very short time of consideration and almost no filtering, I was chosen. After all, it's a chance for me to pay back for all the good thing my dad all these years and still ongoing.

I was, at first, excited to take on the task. The first time I did it, I thought: "Finally this country can escape poverty, this is the way! This gonna save Vietnamese so much time and energy and spend on other meaningful stuff. Therefore, I am doing meaningful work". Trust me, it did and I meant it. But after about 3 times, the excitement went away and I felt like I was taking another boring part-time job. The forms are lengthy, lots fields to be filled, lots pages to be browsed and they are all flaky af. It is not rare when I have done more than halfway and receive silly blocker alert about invalid data and expired session. And if I retried and failed, I might have to recheck if the system is back on everal hours later. Goshh.. as if my 9-5 grinding was not dreadful enough.

On the brink of my future flooded with tasteless work, I have to bring out the best of me to help automate away these numb works which require no more than an emotionless machine who can do the same things so many times without feeling miserable.

# The revelation

First idea most of the times does not work out, I tried to use an automate browser like Playwright and its kind but turned out they are very bad for going to any site and do errands for several reasons:

- Production web does not welcome robots and it is a solven math. A normal command to find and click an element on the website is way harder than it should be: page took too long to load, UI shown in headless is different compared to what I see from normal browser. No surprise, it is very easy to tell based on the user agent of that browser and as a maker I would not want my product to be filled with bots spam.

- Fully automation solution is expensive and not that necessary: 90% of the work I want to automate is very simple, just help me click buttons and fill in fields in form. The rest 10% I can do it myself and they are most of the time hard to automate, things like entering captcha, moving output of an app to another app, detect text from images, etc.. Meanwhile, the automation browser would not let me infere to help my automation easily because they are designed to be able to run from an UI-less environment like Jenkins.

Luckily for me, I have made several Chrome Extension in the past and this time something tickled my mind. I just have a feeling that a chrome extension can help me achieve what I want. So I start another repo and cranks things up again.

And it is exactly what I was looking for - an webapp automation tool made for personal usage.
Take a look.

<iframe width="560" height="315" src="https://www.youtube.com/embed/zc65Qsi_5nY?si=G5j7D66NrLPS-K0j" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

As you can see, I was hand-free while the chrome extension lead me all the way to the OTP prompt. After this step, it carry on to help me fill out several lengthy forms, saving sanity and yawns. All the automation conducted are simple but effective leaving complicated tasks for human or more sophisticated tools (FYI I use Telegram to help detect text from image, which become the input for the automation).

# Semi-automation is not much but it works

Having said that, ever since the extensions I can help my dad with less mental struggle. The moral of story is that from now me and you can leverage more from this kind of application. I will leave the open-source for this project below, there is some tricky processing to simulate typing actions on app written by ReactJs but overall it is not rocket science. Another headsup is that Chrome Extension is well-documented yet CoPilot seem not so good at it, remember to double check when in doubt then.

# Reference

Github code: https://github.com/coolcorexix/automate-dichvucong
