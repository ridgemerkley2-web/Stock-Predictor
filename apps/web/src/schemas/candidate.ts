import { z } from "zod";

export const CandidateSchema = z.object({
  ticker: z.string(),
  side: z.enum(["buy", "sell"]),
  entry_hint: z.number(),
  stop: z.number(),
  target: z.number(),
  ev: z.number(),
  certainty: z.number().min(0).max(1),
  rationale: z.array(z.string()),
  timestamp: z.string(),
});

export type Candidate = z.infer<typeof CandidateSchema>;
