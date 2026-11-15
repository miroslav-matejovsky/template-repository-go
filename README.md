# Template Repository

Starter repository for Go applications with shared development checks and tooling.

Install [mise](https://mise.jdx.dev/getting-started.html), then run:

```text
mise trust
mise install
mise run all
```

Use `mise tasks ls` to list tasks, `mise run test` to run tests, and
`mise run run` to start the example application.

See [development tooling](docs/tooling.md) for configuration, maintenance, and
release commands. The [documentation index](docs/README.md) lists technical guides.

## How to use the dev folder for agentic development

The `dev` folder contains a blueprint for effectively organizing and managing agentic development tasks and workflows.

The main idea is that nothing there is specific to agentic development. The same ideas are applicable to human teams as well. The main difference is that LLMs are significantly faster and therefore need more frequent guidance and oversight.

My flow usually starts with an idea or an assignment. Before I dive into the details, I use `dev/study` and create a prompt that explores the topic and gathers relevant information and insights before moving on to implementation.

The prompt usually contains facts that I already know, information gathered from other repositories, real data, and basically anything that can help the agent understand the context and make informed decisions.

Then I instruct the agent to fill in the gaps with additional research and insights, make recommendations, and propose the next steps for implementation. I especially ask it to put questions and uncertainties, together with recommendations, into a separate file so that I can review and address them systematically.

These questions are important signals that often point to wrong assumptions or gaps in my understanding. This often leads me to discard the study and start again with a revised prompt focused on clarifying assumptions and filling knowledge gaps.

After I am satisfied with the study and the clarified assumptions, I move on to the implementation plan. I instruct the agent to create a detailed plan, breaking the work down into manageable steps and identifying dependencies and potential challenges.

In the last step, I execute the plan, monitor progress, and make adjustments as needed. I often do this manually, one step at a time, briefly reviewing the changes when something unexpected occurs or when I need to provide additional guidance to the agent.

This may look very inefficient at first glance, but it allows for careful oversight and helps ensure that the agent's actions align with the intended plan. Over time, this process helps refine both the agent's performance and my own understanding of the tasks at hand. Also see [Ironies of Automation](https://en.wikipedia.org/wiki/Ironies_of_Automation) for a better understanding of the trade-offs involved in automation and the need for human oversight.

The `bugs` and `backlog` folders are used to track known issues and improvements that are not urgent or immediate. They are usually useful as references during the study and planning phases.

## Links

- [HTMX and Go for WebUI](https://www.alexedwards.net/blog/how-i-use-htmx-with-go)
- [Ironies of Automation](https://en.wikipedia.org/wiki/Ironies_of_Automation)
