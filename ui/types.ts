export type AgentStatus = {
  round: number;
  step: string;
};

export type AgentLog = {
  timestamp: Date;
  message: string;
  round: number;
  idx?: number;
};

export type Objective = {
  topic: string;
  expertise: number;
};

export type Resource = {
  url: string;
  description: string;
  visited: boolean;
};

export type Findings = {
  generated_objectives: Objective[];
  narrative: string;
  remark: string;
};

export type LLMLog = {
  prompt: string;
  response: string;
  idx?: number;
};

export type Narrative = {
  markdown: string;
};

export type AgentState = {
  start_time: string;
  end_time: string;
  agent_role: string;
  status: AgentStatus;
  objectives: Objective[];
  findings: Findings;
  agent_logs: AgentLog[];
  narratives: Narrative[];
  resource_pool: {
    resources: Resource[];
  };
  llm_logs: LLMLog[];
};
