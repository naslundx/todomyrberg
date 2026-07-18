export interface User {
  id: number;
  username: string;
}

export interface Task {
  id: number;
  title: string;
  user_ids: number[];
  status: "pending" | "done";
  due_date: string;
  details: string | null;
  emoji: string | null;
  is_recurring: boolean;
  interval_type: "days" | "weeks" | "months" | "years" | null;
  interval_value: number | null;
  specific_day: number | null;
  created_at: string;
}
