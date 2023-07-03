import { createContext } from "react";
import {
  AgentState,
  AgentStatus,
  Objective,
  Findings,
  AgentLog,
  LLMLog,
  Narrative,
  Resource,
} from "@/types";

export type BlockAGIDataType = {
  start_time: Date;
  end_time: Date | null;
  is_live: boolean;
  is_done: boolean;
  objectives: Objective[];
  generated_objectives: Objective[];
  findings: Findings;
  narratives: Narrative[];
  agent_logs: AgentLog[];
  llm_logs: LLMLog[];
  status: AgentStatus;
  links: Resource[];
};

export const initialData: BlockAGIDataType = {
  is_live: false,
  is_done: false,
  start_time: new Date(),
  end_time: new Date(),
  objectives: [],
  generated_objectives: [],
  findings: {
    generated_objectives: [],
    narrative: "",
    remark: "",
  },
  narratives: [],
  agent_logs: [],
  llm_logs: [],
  status: { step: "PlanChain", round: 0 },
  links: [],
};

export const DataContext = createContext<BlockAGIDataType>(initialData);

function stripCodeBlock(markdown: string) {
  // Strip out the code blocks
  const regex = /```*[\n]*(.*?)[\n]*```*/gs;
  const match = regex.exec(markdown);
  return match ? match[1].trim() : markdown.trim();
}

export const fetchData = async (): Promise<BlockAGIDataType | null> => {
  try {
    const response = await fetch("http://localhost:8888/api/state");
    const data: AgentState = await response.json();

    return {
      is_live: true,
      is_done: !!data.end_time,
      start_time: new Date(data.start_time + "Z"),
      end_time: data.end_time ? new Date(data.end_time + "Z") : null,
      objectives: data.objectives || [],
      generated_objectives: data.findings.generated_objectives || [],
      findings: data.findings,
      // Some narratives have code blocks, which we want to strip out
      narratives:
        data.narratives?.map?.(({ markdown }) => ({
          markdown: stripCodeBlock(markdown),
        })) || [],
      agent_logs: data.agent_logs.map((log, idx) => ({
        ...log,
        timestamp: new Date(log.timestamp + "Z"),
        idx,
      })),
      llm_logs: data.llm_logs.map((log, idx) => ({ ...log, idx })),
      status: data.status || { step: "PlanChain", round: 0 },
      links: data.resource_pool.resources,
    };
  } catch (error) {
    return null;
  }
};
