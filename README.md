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

`dev` folder contains a blueprint for effectively organizing and managing agentic development tasks and workflows.
The main idea is that nothing there is for agentic development.
The ideas are applicable to human teams as well, the main difference is that LLMs are significantly faster and need more frequent guidance and oversight.

My flow usually starts with an idea or assignment. Before I dive into details i use 'dev/study' and create a prompt that explores the topic and 
gathers relevant information and insights before moving on to implementation.

the prompt usually contains a facts that I already know, gather information from other repositories, real data,
basically everything that can help the agent understand the context and make informed decisions.
Then I instruct the agent to fill in the gaps with additional research and insights, make recommendations, and propose next steps for implementation.
I especially ask to put questions and uncertainties with recommendations to separate file so that I can review and address them systematically.

These questions are important signals that often points to wrong assumptions or my gaps in understanding.
This often leads to removing the study and start with revisited prompt that is focused on clarifying assumptions and filling knowledge gaps.

After I am satisfied with the study and the clarified assumptions, I move on to the plan for implementation.
I instruct the agent to create a detailed plan for implementation, breaking down tasks into manageable steps and identifying dependencies and potential challenges.

And in the last step I execute the plan, monitor progress, and make adjustments as needed.
Often manually one by one, I briefly review the changes if something unexpected occurs or if I need to provide additional guidance to the agent.

This looks very inefficient at first glance, but it allows for careful oversight and ensures that the agent's actions align with the intended plan. Over time, this process helps in refining both the agent's performance and my own understanding of the tasks at hand. Also see [Ironies of Automation](https://en.wikipedia.org/wiki/Ironies_of_Automation).

## Links

- [HTMX and Go for WebUI](https://www.alexedwards.net/blog/how-i-use-htmx-with-go)
- [Ironies of Automation](https://en.wikipedia.org/wiki/Ironies_of_Automation)
