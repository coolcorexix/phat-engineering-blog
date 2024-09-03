---
layout: post
title: Hold on, you might not need a monorepo for your SaSS
date: 2024-09-03 11:07:49 +0700
categories: []
---
## when to use it, originally?

+ to use with really, really big monorepo from big organization
where the code is very thick and then relationship is way beyond
manual inspecting. For example: Google, Facebook
+ to control the publishment of mutiple npmjs libraries which need to
compatible / dependancy-harmonized with each other when get used. For example: https://github.com/facebook/react
++ react 17.0.4 HAVE TO GO WITH react-dom 17.0.4 and these monorepoes help the makers
make sure that everything work in one single commit (atomic commit people talk about)
 

## in the case of a SaaS with multiple repos,
should we apply a monorepo?
+ in the case of saleshood, a company I am working for rn, it is not either: 
    too big to manually control the relationship, nor
    having to manage multiple OS libraries
so it seems like the monorepo won't bring as much benefit as its new problem

## what is the cheaper alternative?
But we really want to get rid of the multiple / having-to-build-first repos, what can we do?
+ current approaches: multiple vite.config files and clear responsibility boundary for "main" folders.
By this way, shared code can be directly imported as Typescript, taking instant effects and from one repo
multiple apps/services can be built and deployed

+ challenges ahead:
    How to make CI/CD work as-is? 
    In the past, there is a huge benefit of loose coupling between repos: with multiple versions of a uikit, 
the repos that does not need the new version won't have to update commit hash and put in the adaptation 
effort which is sensible. 
How do we keep that after the change? Should we consider sacrificing this benefit for a leaner setup? is this the right trade off?    