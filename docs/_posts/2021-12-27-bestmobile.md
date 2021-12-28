---
title: "(in progress) Ideal mobile desktop for Secure development."
date: 2021-12-27
classes: wide
---

## What is best mobile desktop for Secure development

An environment which can be carried to everywhere with ease within small bag, but has ability to access company data and good for coding, i.e easy to type many characters and moving  cursor fast.

And also, data is accessed remotely with evaluation of every data access by remote server or local data could be encrypted and be wiped when lost or stolen.

## The candidate

I chose 7inch - 8inch terminals are the best.

* (iOS) iPad Mini 6th Gen.
* (Ubuntu) Onemix 3s with Ubuntu.
* (Android) Astro Slide 5G.

## iPad Mini 6th Gen

Good environment to access business data. Good environment for coding.

Best if we had **Arrow** key. Good OSK especially in vertical mode, Steve I pray if you had said **I need Arrow key** in early days of iPhone development.

* Deployment example.
  * Deploy with AppleBusinessManager+Intune.
  * Access company data of daily use with managed MSOffice.
  * Use Windows 365 desktop with RDClient for secured data.
  * Code using WorkingCopy+Texastic.

* Detailed evaluation
  * Security
    * Local data protection
      * Data encrypton    : ok (enabled by default)
      * Auto lock         : ok (and can be forrced by MDM)
      * Local wipe        : ok (when try exceeds a limit)
      * Remote wipe       : ok (when with SIM)
      * Search lost device: Find My
    * Remote data protection
      * Limit use of company data within managed Apps.
        * O365 apps
        * Web apps on MS Edge
        * WVD/AVD client for iOS
    * Need improvement
      * RD client for iOS: touch offset glitch
        * Touch offcet is different approx. 5-10px from actual location, I have proposed improvement in feedback hub, but...
      * Expecting more managed apps:
        * Slack
        * Textastic
        * WorkingCopy
        * iSH
  * Functionality
    * Hardware
      * Reliable, robust form factor
      * Long battery life, that can be used all day long
    * Now we can do every task for office workers.
      * O365
      * Slack
      * Textastic
      * WorkingCopy
      * iSH

Here are/ tips for good deployment.

* **Before you by iPad**, get DUNs number and apply Apple business manager, then **buy iPad with SIM model** **from Apple store using ABM account**. Company purchased devices with SIM are easily managed by MDM.
* XXX
* XXX
* XXX

## Onemix 3s with Ubuntu

If you use Onemix with Win10, UX is terrible because font quality and placement within UI still needs to be improved in unacceptable level in this small size display. But UX is dramatically improved when you use it with Ubuntu. Recent Ubuntu UI is beautiful and easy to read characters. Small CPU power consumption is also attractive.

Still iPad Mini Gen6 exceeds in every aspect, especially in security, but the lack of **Arrow key** make this setup more attractive.

With Win10, Font of UI is unacceptable, as characters is hard to read, so font size need to be bigger compared to other setups, i.e. there is smaller working area. CPU concurrently running nearly 90%, so FAN noise and thermal is bad.

I need to add an important comment, the caveats above is acceptable, moreover I even did not notice them with normal sized mobile PCs and Desktop PCs. 7inch sized small PC and trying to use it as business makes this perspective as "problem".

* Deployment example.
  * Disk is encrypted during installation,
* Detailed evaluation
  * Security
    * Local data protection
      * Data encrypton    : ok (can be enabled during installation.)
      * Auto lock         : ok (and can be forrced by MDM)
      * Local wipe        : ???
      * Remote wipe       : ???
      * Search lost device: ???
    * Remote data protection
      * ???
        * VS codespace
    * Need improvement
      * ???
  * Functionality
    * Reliable, robust form factor
    * Now we can do every task for office workers.
      * ??? - O365
      * ??? - Slack
      * **vscode**

* tasks to complete evaluation (i.e. candidate of Cons.)
  * [ ] WVD/AVD access using some rdp client
  * [ ] Wype locally or remotely
  * [ ] Enable hybernation
  * [ ] Remote access file storage
    * (which requires concurrent connection to host git local repository)
  * [ ] Others
    * [ ] Find My using AirTag
    * [ ] Embed SIM in M.2 Slot
    * [ ] Extending battery life (Approx. 2.5hrs ... )

Here are tips for good deployment.

* Screen inverted
  * -> use "xrandr -o left"
* OSK(On screen keyboard) appears everytime I have touched display
  * -> disable it using gnome extension <https://askubuntu.com/questions/965250/on-screen-keyboard-popping-up-whenever-i-touch-screen>

## Astro Slide 5G

I am looking forward. This will be the best mobile, although this is still in prototype phase. <https://www.indiegogo.com/projects/astro-slide-5g-transformer#/>

* Hardware keyboard
* MDM support (as this is pure Android)
* SIM for 5G network
