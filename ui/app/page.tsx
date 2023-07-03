"use client";
import React, {
  useEffect,
  useState,
  useContext,
  useCallback,
  useRef,
  forwardRef,
  memo,
} from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import Image from "next/image";
import { DataContext, BlockAGIDataType, fetchData, initialData } from "@/data";
import delay from "delay";
import { AgentLog } from "@/types";
import copy from "copy-to-clipboard";

type CollapsibleProps = {
  icon: string;
  title: React.ReactNode;
  info?: React.ReactNode;
  defaultCollapsed?: boolean;
  autoScroll?: boolean;
  children: React.ReactNode;
};

const Collapsible = forwardRef<HTMLDivElement, CollapsibleProps>(
  function _Collapsible(
    { icon, title, children, info, defaultCollapsed = false }: CollapsibleProps,
    ref
  ) {
    const [collapsed, setCollapsed] = useState(defaultCollapsed);
    const toggle = () => setCollapsed(!collapsed);
    return (
      <div
        className={`transition-all mt-[-1px] flex min-h-[50px] justify-stretch flex-col overflow-hidden ${
          collapsed ? "flex-0 max-h-[50px]" : "flex-1"
        }`}
      >
        <div
          className="select-none flex border-y border-y-bd-1 items-center cursor-pointer min-h-[50px] h-[50px] px-6 transition-all hover:bg-bg-lt"
          onClick={toggle}
        >
          <span className="text-[20px]">{icon}</span>
          <span className="ml-4 font-medium text-[18px]">{title}</span>
          <div className="ml-auto">{info}</div>
          <div className="ml-6">
            <Image
              className={`transition-all transform ${
                collapsed ? "" : "rotate-90 opacity-30"
              }`}
              alt="Chevron"
              src="/chevron.svg"
              height={12}
              width={6}
            />
          </div>
        </div>
        <div
          className="flex-1 overflow-auto shadow-section scroll-smooth"
          ref={ref}
        >
          {children}
        </div>
      </div>
    );
  }
);

function ObjectivesTab() {
  const { objectives, generated_objectives } = useContext(DataContext);

  const expertise =
    objectives.reduce((acc, objective) => acc + objective.expertise, 0) /
    objectives.length;

  return (
    <Collapsible
      icon="⛳️"
      title={
        <div className="flex items-center">
          Objectives
          <span className="inline-block ml-4 px-2 leading-6 rounded bg-fg-1 text-ac-1 font-code font-semibold text-[12px]">
            {generated_objectives.length} intermediate
          </span>
        </div>
      }
      info={
        <span className="font-code text-[14px] font-medium">
          Expertise: {(expertise * 100).toFixed(1)}%
        </span>
      }
      defaultCollapsed={true}
    >
      <div className="py-4 px-6">
        <div className="mb-4 text-ft-2 font-semibold">
          ✍️ User-Defined Objectives
        </div>
        {objectives.map(({ topic, expertise }) => (
          <div key={`${topic}_${expertise}`} className="my-2 flex">
            <div className="block h-fit text-center w-[50px] px-2 leading-6 rounded bg-fg-3 text-ac-3 font-code font-semibold text-[12px]">
              {(expertise * 100).toFixed(1)}%
            </div>
            <div className="flex-1 ml-3 text-16px break-words">{topic}</div>
          </div>
        ))}
        <div className="mt-6 mb-4 text-ft-2 font-semibold">
          📟 Auto-Generated Objectives
        </div>
        {generated_objectives.map(({ topic, expertise }) => (
          <div key={`${topic}_${expertise}`} className="my-2 flex">
            <div className="block h-fit text-center w-[50px] px-2 leading-6 rounded bg-fg-3 text-ac-3 font-code font-semibold text-[12px]">
              {(expertise * 100).toFixed(1)}%
            </div>
            <div className="flex-1 ml-3 text-16px break-words">{topic}</div>
          </div>
        ))}
      </div>
    </Collapsible>
  );
}

function formatTime(date: Date) {
  const hours = date.getHours().toString().padStart(2, "0");
  const minutes = date.getMinutes().toString().padStart(2, "0");
  const seconds = date.getSeconds().toString().padStart(2, "0");

  return `${hours}:${minutes}:${seconds}`;
}

const AgentLogEntry = memo(function _AgentLogEntry({
  timestamp,
  message,
  round,
  idx,
}: AgentLog) {
  const [messageQueue, setMessageQueue] = useState("");
  const [doneAnimating, setDoneAnimating] = useState(false);

  useEffect(() => {
    if (Date.now() - timestamp.getTime() > 3000) {
      setMessageQueue(message);
      setDoneAnimating(true);
      return;
    }

    (async () => {
      for (let i = 0; i < message.length; i++) {
        setMessageQueue(message.slice(0, i + 1));
        await delay(12);
      }
      await delay(350);
      setDoneAnimating(true);
    })();
  }, []);

  return (
    <div
      className={`transition-all flex-0 min-h-0 flex text-[13px] font-code whitespace-pre-wrap break-words items-start py-2 px-3 ${
        doneAnimating ? (idx && idx % 2 ? "bg-bg-2" : "bg-bg-1") : "bg-fg-1"
      }`}
    >
      <div className="w-[80px] text-ft-2 ml-2">{formatTime(timestamp)}</div>
      <div
        className={`transition-all ml-1 px-2 leading-6 rounded font-code font-semibold text-[12px] ${
          doneAnimating ? "bg-fg-3 text-ac-3" : "bg-ac-1 text-fg-1"
        }`}
      >
        {round ? `R#${round}` : "PREPARING"}
      </div>
      <div className="flex-1 ml-3">{messageQueue}</div>
    </div>
  );
});

function StatusTab() {
  const { is_done, status, agent_logs } = useContext(DataContext);

  return (
    <Collapsible
      icon="🌈"
      title={
        <div className="flex items-center">
          Status
          <div className="flex ml-2">
            {["Plan", "Research", "Update", "Narrate", "Evaluate"].map(
              (step) => (
                <div
                  key={step}
                  className={`ml-2 px-2 leading-6 rounded font-code font-semibold text-[12px] ${
                    is_done
                      ? "bg-fg-1 text-ac-1"
                      : status.step.startsWith(step)
                      ? "bg-fg-2 text-ac-2 animate-bounce-fast"
                      : "bg-fg-3 text-ac-3"
                  }`}
                >
                  {step[0]}
                </div>
              )
            )}
          </div>
        </div>
      }
      info={
        <span className="font-code text-[14px] font-medium">
          Round #{status.round}
        </span>
      }
      defaultCollapsed={false}
    >
      <div className="flex flex-col-reverse">
        {agent_logs.map((log) => (
          <AgentLogEntry key={log.timestamp + log.message} {...log} />
        ))}
      </div>
    </Collapsible>
  );
}

function ResourcesTab() {
  const { links } = useContext(DataContext);

  return (
    <Collapsible
      icon="🔗"
      title={
        <div className="flex items-center">
          Resource Pool
          <span className="inline-block ml-4 px-2 leading-6 rounded bg-fg-1 text-ac-1 font-code font-semibold text-[12px]">
            {links.length} links
          </span>
        </div>
      }
      info={
        <span className="font-code text-[14px] font-medium">
          Visited: {links.filter(({ visited }) => visited).length}
        </span>
      }
      defaultCollapsed={true}
    >
      <div className="py-4 px-6">
        <div className="mb-4 text-ft-2 font-semibold">✅ Visited Links</div>
        {links
          .filter(({ visited }) => visited)
          .map(({ url, description }) => (
            <div key={url} className="my-2 flex">
              <div className="block h-fit text-center w-[65px] px-2 leading-6 rounded bg-fg-2 text-ac-2 font-code font-semibold text-[12px]">
                Visited
              </div>
              <div className="flex-1 ml-3 text-16px truncate">
                <a href={url} target="_blank" rel="noreferrer">
                  {description}
                </a>
              </div>
            </div>
          ))}
        <div className="mt-6 mb-4 text-ft-2 font-semibold">
          📥 New Links (Pending Agent Visit)
        </div>
        {links
          .filter(({ visited }) => !visited)
          .map(({ url, description }) => (
            <div key={url} className="my-2 flex">
              <div className="block h-fit text-center w-[65px] px-2 leading-6 rounded bg-fg-3 text-ac-3 font-code font-semibold text-[12px]">
                New
              </div>
              <div className="flex-1 ml-3 text-16px truncate">
                <a href={url} target="_blank" rel="noreferrer">
                  {description}
                </a>
              </div>
            </div>
          ))}
      </div>
    </Collapsible>
  );
}

function LLMLogTab() {
  const { llm_logs } = useContext(DataContext);
  const [autoscroll, setAutoscroll] = useState(true);
  const [scrollDiff, setScrollDiff] = useState(0);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollDiff < 0 && autoscroll) setAutoscroll(false);
  }, [scrollDiff < 0]);

  useEffect(() => {
    if (autoscroll && scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [
    llm_logs.length && llm_logs[llm_logs.length - 1]?.response?.length,
    scrollRef,
    autoscroll,
  ]);

  // Keep track of the scroll diff
  useEffect(() => {
    let lastScroll = 0;
    function setScroll() {
      const scroll = scrollRef?.current?.scrollTop || 0;
      setScrollDiff(scroll - lastScroll); // positive if scrolling down
      lastScroll = scroll;
    }
    scrollRef?.current?.addEventListener("scroll", setScroll, false);
    return () =>
      scrollRef?.current?.removeEventListener("scroll", setScroll, false);
  }, [scrollRef]);

  return (
    <Collapsible
      icon="🤖"
      title="LLM Log"
      info={
        <div className="flex items-center">
          <span className="font-code text-[14px] font-medium mr-3">
            Autoscroll
          </span>
          <label className="relative flex items-center cursor-pointer">
            <input
              type="checkbox"
              checked={autoscroll}
              className="sr-only peer"
              onChange={(e) => {
                setAutoscroll(e.target.checked);
              }}
            />
            <div
              className={
                "w-11 h-6 bg-fg-3 border border-ft-2 rounded-full peer " +
                "peer-checked:ring-2 peer-checked:ring-fg-1 " +
                "peer-checked:after:translate-x-full peer-checked:after:border-white peer-checked:bg-ac-1 " +
                "after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-bg-1 after:border-ft-2 after:border after:rounded-full after:h-5 after:w-5 after:transition-all"
              }
            ></div>
          </label>
        </div>
      }
      defaultCollapsed={false}
      ref={scrollRef}
    >
      <div className="min-h-full bg-bg-2 whitespace-pre-wrap py-4 px-6 font-code text-[13px] leading-[16px]">
        {llm_logs.slice(-20).map(({ idx, prompt, response }) => (
          <>
            <div className="flex my-4 items-center">
              <div className="border-t-2 border-t-ac-1 flex-1"></div>
              <div className="mx-3 text-ac-1 font-semibold">
                Prompt #{(idx || 0) + 1}
              </div>
              <div className="border-t-2 border-t-ac-1 flex-1"></div>
            </div>
            <div
              key={`${idx}-prompt-${prompt.length}`}
              className="my-3 text-ft-2 transition-all break-words"
            >
              {prompt}
            </div>
            <div
              key={`${idx}-reponse-${response.length}`}
              className="my-3 text-ft-1 transition-all break-words"
            >
              {response}
            </div>
          </>
        ))}
      </div>
    </Collapsible>
  );
}

function Header() {
  const { is_live, is_done } = useContext(DataContext);
  return (
    <div className="flex mt-4 mb-8">
      <div>
        <div className="flex">
          <div className="inline-flex">
            <Image
              alt="BlockAGI Logo"
              src="/blockagi.svg"
              width={44}
              height={44}
            />
          </div>
          <div className="ml-4 tracking-wide">
            <div className="font-bold text-[22px] leading-7 bg-clip-text text-transparent bg-gr-1">
              BlockAGI
            </div>
            <div className="font-bold text-[18px] text-ft-1">
              Your Self-Hosted, Hackable Research Agent
            </div>
          </div>
        </div>
      </div>
      <div className="ml-auto">
        <span
          className={`inline-block px-2 leading-6 rounded font-code font-semibold text-[12px] ${
            is_done
              ? "bg-fg-1 text-ac-1"
              : is_live
              ? "bg-fg-2 text-ac-2"
              : "bg-fg-4 text-ac-4"
          }`}
        >
          {is_done
            ? "AGENT FINISHED"
            : is_live
            ? "AGENT RUNNING"
            : "AGENT STOPPED"}
        </span>
      </div>
    </div>
  );
}

function Operation() {
  return (
    <section className="min-w-0 flex-1 flex flex-col justify-stretch mx-auto px-12 max-w-[760px]">
      <Header />
      {/* Main */}
      <div className="flex flex-col min-h-0 flex-1 rounded-md border border-bd-1 overflow-hidden">
        <StatusTab />
        <ObjectivesTab />
        <ResourcesTab />
        <LLMLogTab />
      </div>
      {/* Footer */}
      <div className="flex items-center mt-6 font-bold text-ft-2">
        <div className="flex space-x-12">
          <a href="https://github.com" target="_blank">
            Github
          </a>
          <a href="https://github.com" target="_blank">
            Documentation
          </a>
        </div>

        <div className="flex items-center ml-auto font-semibold text-ft-1 text-[15px]">
          Brought to you by{" "}
          <a
            className="inline-flex ml-2 hover:text-ac-2 hover:decoration-ac-2 group"
            href="https://blockpipe.io"
            target="_blank"
          >
            <div className="inline-flex mr-1 group-hover:animate-spin-fast">
              <Image
                alt="Blockpipe Logo"
                src="/blockpipe.svg"
                width={18}
                height={18}
              />
            </div>
            Blockpipe
          </a>
        </div>
      </div>
    </section>
  );
}

type NarrativeMarkdownProps = {
  children: string;
};

const NarrativeMarkdown = memo(function _NarrativeMarkdown({
  children = "",
}: NarrativeMarkdownProps) {
  return (
    <ReactMarkdown
      remarkPlugins={[remarkGfm]}
      components={{
        h1: ({ node, ...props }) => (
          <h2 {...props} className="font-medium text-[24px] mt-6 mb-2" />
        ),
        h2: ({ node, ...props }) => (
          <h2 {...props} className="font-bold text-[20px] mt-6 mb-2" />
        ),
        h3: ({ node, ...props }) => (
          <h2 {...props} className="font-semibold text-[18px] mt-4 mb-2" />
        ),
        ul: ({ node, ...props }) => (
          <ul
            {...props}
            className="list-image-[url(/list.svg)] list-outside pl-7"
          />
        ),
        ol: ({ node, ...props }) => (
          <ol
            {...props}
            className="list-decimal list-outside marker:bg-ac-1  pl-8 marker:font-code marker:font-bold marker:text-[15px]"
          />
        ),
        blockquote: ({ node, ...props }) => (
          <blockquote
            {...props}
            className="border-l-4 border-bd-1 pl-4 font-code text-[12px] text-ft-2 mb-8 transition-all hover:border-ac-1 hover:text-ft-1"
          />
        ),
        li: ({ node, ...props }) => <li {...props} className="" />,
        p: ({ node, ...props }) => <p {...props} className="mt-2 mb-4" />,
        a: ({ node, ...props }) => (
          <a
            {...props}
            className="text-ac-1 font-bold relative z-[0]"
            rel="noreferrer"
            target={props?.href?.startsWith("#") ? "_self" : "_blank"}
          />
        ),
        sup: ({ node, children, ...props }) => (
          <sup {...props} className="ml-1 text-[0.8em]">
            [{children}]
          </sup>
        ),
      }}
    >
      {children}
    </ReactMarkdown>
  );
});

function Narrative() {
  const [numOptions, setNumOptions] = useState(0);
  const [selectedIdx, setSelectedIdx] = useState(0);
  const { narratives } = useContext(DataContext);
  const narrative = narratives[selectedIdx]?.markdown || "";

  const [copied, setCopied] = useState(false);

  useEffect(() => {
    setSelectedIdx(narratives.length - 1);
    setNumOptions(narratives.length);
  }, [narratives.length > 0]);

  useEffect(() => {
    if (narratives.length < numOptions) {
      setSelectedIdx(0);
    } else if (narratives.length > numOptions) {
      if (selectedIdx === numOptions - 1) setSelectedIdx(narratives.length - 1);
    }
    setNumOptions(narratives.length);
  }, [narratives.length, selectedIdx, numOptions]);

  const copyMarkdown = useCallback(() => {
    copy(narrative);
    setCopied(true);
    setTimeout(() => setCopied(false), 1000);
  }, [narrative]);

  return (
    <article className="min-w-0 min-h-full w-full flex-1 rounded-lg shadow-article bg-bg-2 overflow-auto scroll-smooth max-w-[760px] relative">
      <div
        className={`sticky relative z-[100] flex items-end font-code text-[14px] transition-all ${
          narrative ? "top-0" : "top-[-80px] mt-[-80px]"
        } left-0 right-0 h-[80px] px-16 py-6 bg-gradient-to-b from-[rgba(247,247,247,1)] via-[rgba(247,247,247,0.95)] via-80% to-[rgba(247,247,247,0)]`}
      >
        <div
          className="flex items-center text-ft-2 cursor-pointer hover:opacity-80 transition-all mb-1"
          onClick={copyMarkdown}
        >
          <Image alt="Copy" src="/copy.svg" height={24} width={24} />
          <div
            className={`ml-2 transition-all ${
              copied ? "text-ft-1 font-semibold" : ""
            }`}
          >
            {copied ? "Copied to Clipboard" : "Copy as Markdown"}
          </div>
        </div>
        <div className="ml-auto flex items-center">
          <Image alt="Ref" src="/ref.svg" height={24} width={24} />
          <div className="mr-2 ml-2 text-ft-2">Report from</div>
          <select
            value={selectedIdx}
            className="font-code text-ft-1 border border-bd-1 outline-0 w-[110px] transition-all hover:border-ac-1 text-center h-[32px] rounded-md text-[14px]"
            onChange={(e) => setSelectedIdx(parseInt(e.target.value))}
          >
            {narratives.map((_, idx) => (
              <option value={idx} key={idx}>
                Round #{idx + 1}
              </option>
            ))}
          </select>
        </div>
      </div>
      <div className="z-[0] w-full px-16 pb-12">
        {narrative ? (
          <NarrativeMarkdown>{narrative}</NarrativeMarkdown>
        ) : (
          <div className="h-[420px] flex items-center justify-center">
            <div className="font-bold text-center text-ft-2 animate-pulse text-[24px]">
              🤔 Agent Thinking and Researching ...
            </div>
          </div>
        )}
      </div>
    </article>
  );
}

export default function Home() {
  const [data, setData] = useState<BlockAGIDataType>(initialData);

  useEffect(() => {
    const interval = setInterval(async () => {
      const newData = await fetchData();
      if (newData) setData(newData);
      else setData((prevData) => ({ ...prevData, is_live: false }));
    }, 200);
    return () => clearInterval(interval);
  }, []);

  return (
    <DataContext.Provider value={data}>
      <main className="flex max-h-screen min-h-screen items-stretch font-sans p-8">
        <Operation />
        <Narrative />
      </main>
    </DataContext.Provider>
  );
}
