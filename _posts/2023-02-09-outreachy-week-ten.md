---
title: "Outreachy: Week ten"
description: In this week’s article, I share an overview of the Wagtail user guide documentation project and the various skills I learnt while working on the project.
date: 2023-02-09 00:00:00 +0100
categories: [Open Source, Outreachy]
tags: [open-source]
pin: false
image:
  path: /assets/img/cover-images/cover-image-outreachy.jpg
  alt: Cover image displaying the logos of Open Source, Wagtail, and Outreachy.
published: true
---

I have three weeks left to complete my [Outreachy](https://www.outreachy.org/) internship with [Wagtail](https://wagtail.org/).

In my [last article](/posts/outreachy-week-nine), I discussed how I got started learning the technologies behind Wagtail CMS.

In this week’s article, I share an overview of the Wagtail user guide documentation project and the various skills I learnt while working on the project. I also share the tasks I worked on this week and the highlights of my tasks for next week.

## Overview of the user guide documentation project

As a result of my internship with Wagtail, I have gained invaluable experience. Having learnt so much in such a short time, I now feel more confident about the future. Also, I'm more prepared to handle new challenges.

I started my internship experience by working on making improvements to the user guide documentation of the Wagtail CMS. As a result of working on the user guide documentation, I have developed my writing skills to a level I never imagined possible.

As part of the process of improving the user guide documentation, my mentors had me conduct a gap analysis. The purpose of the gap analysis is to identify deficiencies in the user guide documentation and suggest ways to improve it. To identify the deficiencies, I compared and contrasted the current state of the user guide documentation with its expected state. After completing the gap analysis, I wrote a [report](https://github.com/wagtail/guide/issues/287#issuecomment-1350186679) about my findings. The purpose of the report is to make sure that the other members of the Wagtail community are aware of my findings and to get their feedback as well.

One of the deficiencies I identified after conducting the gap analysis is the inconsistencies in the grammar and tone of the user guide documentation. To help with this, I proposed two writing style guides to make the necessary improvements. These two writing style guides are the [Microsoft Writing Style Guide](https://learn.microsoft.com/en-us/style-guide/welcome/) and the [Google developer documentation style guide](https://developers.google.com/style). After examining the details of both writing style guides, I came to the conclusion that the Google developer documentation style guide is the best fit for the Wagtail user guide project. I wrote a [report](https://github.com/wagtail/guide/discussions/282#discussioncomment-4332158) on this, and the [Wagtail core team](https://wagtail.org/core-team/) approved my preference.

I also conducted some user research on the user guide documentation with the help of my mentors. The goal of the user research is to get some feedback from the users of the user guide documentation. One of my mentors, [Jonny](https://github.com/jonnypeaks), explained to me what user research is all about and some of the methodologies that I can adopt to get helpful feedback.

For the documentation project, we adopted three user research methodologies: surveys, screening, and interviews. Surveys aid in understanding the macro expectations of Wagtail users, while interviews aid in understanding their micro expectations. Screening the responses from both user-research methods ensures that the team analyzes the responses in the right way. Screening also helps in closing the error gap.

## Week ten in review

This week, I solved three of the four programming tasks given to me by my mentors. The fourth task is Django-based, a framework that I’m yet to learn. The goal of the programming tasks is to test how far I have gone with understanding the technologies behind the Wagtail CMS, especially Python.

The first programming task is to generate a list of combinations from a list of Wagtail locales (\["en", "is", "en\_GB"\]) and versions (\["latest", "4.1.x", "4.2.x"\]):

```python
def generate_combinations(locales, versions):
    combined_list = []
    for locale in locales:
        for version in versions:
            combined_list.append(f"{locale}-{version}")
    return combined_list
```

The second programming task is to generate a dictionary that has the combinations generated in programming task one. This time the combinations should be split into their versions and locales:

```python
def split_versions_and_locales(versions_with_locales):
    results = []
    for combination in versions_with_locales:
        split_item = combination.split("-")
        results.append({
            "version": split_item[0],
            "locale": split_item[1]}
        )
    return results
```

The third programming task is about generating a CSV file ready to import with Wagtail’s bulk redirects importer, given a list of locales (\["en", "is", "en\_GB"\]), and a list of versions (\["latest", "4.1.x", "4.2.x"\]):

```python
import csv

locales = ["en", "is", "en_GB"]
versions = ["latest", "4.1.x", "4.2.x"]

def generate_combinations(locales, versions):
    combined_list = []
    for locale in locales:
        for version in versions:
            combined_list.append(f"{locale}-{version}")
    return combined_list

def create_csv():
    list = generate_combinations(locales, versions)
    with open("combinations.csv", 'w') as file:
        writer = csv.writer(file)
        return writer.writerow(list)

create_csv()
```

In order to solve the fourth task, I had to start learning Django. At the moment, I’m going through the quickstart tutorial on the Django documentation.

## The week ahead

My task for next week is simple; continue my learning of the Django framework and solve the fourth programming task.

> Read more about my Outreachy internship experience with Wagtail in my ongoing [series of articles](/categories/outreachy).
