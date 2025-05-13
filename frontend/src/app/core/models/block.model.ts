export interface Choice {
  id: string;
  label: string;
  editing?: boolean;
}

export interface Reply {
  id: string;
  character: string;
  text: string;
  tone: string;
}

export interface Block {
  id: number;
  parentId?: number;
  linkedChoiceId?: string;
  choices: Choice[];
  replies?: Reply[];
  position?: { x: number; y: number };
  command?: string;
}