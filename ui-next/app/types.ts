interface Message {
    role: string;
    content: string;
}

interface SessionFetchAPIResponse {
    _session_id: string;
    _context: string;
    summary: string;
    key_entities: string[];
    messages: Message[];
}