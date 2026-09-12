const API_BASE_URL =
  import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  const text = await response.text();
  let data = {};
  try {
    data = text ? JSON.parse(text) : {};
  } catch {
    data = { detail: text || "Unexpected server response." };
  }

  if (!response.ok) {
    throw new Error(data.detail || `Request failed (${response.status})`);
  }

  return data;
}

export const api = {
  createProfile: (profile) =>
    request("/profile/", {
      method: "POST",
      body: JSON.stringify(profile),
    }),

  getProfile: (profileId) => request(`/profile/${profileId}`),

  updateProfileDetails: (profileId, details) =>
    request(`/profile/${profileId}/details`, {
      method: "PUT",
      body: JSON.stringify(details),
    }),

  match: (profileId) =>
    request("/match/", {
      method: "POST",
      body: JSON.stringify({ profile_id: Number(profileId) }),
    }),

  getSchemes: () => request("/schemes/"),

  getPartners: ({ state = "", district = "", schemeId = "" } = {}) => {
    const params = new URLSearchParams();
    if (state) params.set("state", state);
    if (district) params.set("district", district);
    if (schemeId) params.set("scheme_id", schemeId);
    const query = params.toString();
    return request(`/partners/${query ? `?${query}` : ""}`);
  },

  calculateEmi: (loanAmount, interestRate, tenureYears) =>
    request("/emi/", {
      method: "POST",
      body: JSON.stringify({
        loan_amount: Number(loanAmount),
        interest_rate: Number(interestRate),
        tenure_years: Number(tenureYears),
      }),
    }),
};

export { API_BASE_URL };
