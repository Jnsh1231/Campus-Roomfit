"""Campus Roomfit - a CS1 Drafter roommate and study-partner matcher.

Run: python3 campus_roomfit.py
Install first if needed: python3 -m pip install drafter
Profiles are saved in browser storage in BlockPy, or campus_match_profiles.json on desktop.
"""

from dataclasses import dataclass, field, asdict
import json
import sys
from pathlib import Path
from uuid import uuid4
from drafter import *


@dataclass
class Profile:
    name: str
    looking_for: str
    sleep: str
    cleanliness: str
    noise: str
    guests: str
    smoking: str
    bio: str
    profile_id: str = ""


@dataclass
class State:
    current_profile: Profile | None = None
    profiles: list[Profile] = field(default_factory=list)
    editing_id: str = ""
    match_filter: str = "Same goal"


def example_profiles() -> list[Profile]:
    """Fictional students used to demonstrate the matching feature."""
    return [
        Profile("Maya R.", "Roommate", "Early bird", "Very tidy", "Quiet",
                "Yes", "No", "I like morning classes, tidy spaces, and quiet evenings."),
        Profile("Daniel K.", "Roommate", "Early bird", "Moderately tidy", "Quiet",
                "No", "No", "I like early classes, gaming, and keeping my room organized."),
        Profile("Priya S.", "Roommate", "Night owl", "Very tidy", "Quiet",
                "Yes", "No", "I enjoy reading, art, and a peaceful living space."),
        Profile("Alex T.", "Study partner", "Night owl", "Moderately tidy", "Some noise",
                "Yes", "No", "I like studying with other people and sharing ideas."),
        Profile("Taylor M.", "Roommate", "Early bird", "Very tidy", "Quiet",
                "Yes", "No", "I like early mornings and keeping shared spaces clean."),
        Profile("Sam P.", "Study partner", "Early bird", "Very tidy", "Quiet",
                "No", "No", "I prefer focused library sessions and short breaks."),
    ]


# BlockPy runs Drafter in a browser (Pyodide), where __file__ is not defined.
# Use localStorage there; use a JSON file when running normal desktop Python.
# The browser version runs Python through Pyodide (an advanced technique).
# Desktop Python writes JSON to disk; the browser version uses localStorage.
# Both are single-device demos, not a multi-user online database.
BROWSER_MODE = sys.platform == "emscripten"
STORAGE_KEY = "campus_roomfit_profiles_v1"
if not BROWSER_MODE:
    DATA_FILE = Path(__file__).with_name("campus_match_profiles.json")


def read_saved_data() -> dict | None:
    """Return saved profile data or None if there is nothing saved yet."""
    if BROWSER_MODE:
        try:
            from js import localStorage
            raw = localStorage.getItem(STORAGE_KEY)
            return json.loads(str(raw)) if raw is not None else None
        except Exception:
            # Some school preview frames block browser storage.
            return None
    if DATA_FILE.exists():
        try:
            return json.loads(DATA_FILE.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return None
    return None


def save_profiles(state: State) -> None:
    """Save all profiles and the selected profile."""
    data = {
        "profiles": [asdict(profile) for profile in state.profiles],
        "active_id": state.current_profile.profile_id if state.current_profile else "",
    }
    if BROWSER_MODE:
        try:
            from js import localStorage
            localStorage.setItem(STORAGE_KEY, json.dumps(data))
        except Exception:
            # Keep using Drafter State when localStorage is disabled.
            pass
    else:
        temporary = DATA_FILE.with_suffix(".json.tmp")
        temporary.write_text(json.dumps(data, indent=2), encoding="utf-8")
        temporary.replace(DATA_FILE)


def load_profiles() -> State:
    """Restore existing students or start with fictional sample profiles."""
    data = read_saved_data()
    if data is not None:
        profiles = [Profile(**item) for item in data.get("profiles", [])]
        active_id = data.get("active_id", "")
    else:
        profiles = example_profiles()
        active_id = ""
    for profile in profiles:
        if not profile.profile_id:
            profile.profile_id = uuid4().hex
    # `next` and the generator expression find the first matching ID.
    # If no ID matches, None is returned instead of raising an error.
    current = next((p for p in profiles if p.profile_id == active_id), None)
    state = State(current_profile=current, profiles=profiles)
    if data is None:
        save_profiles(state)
    return state


def refresh(state: State) -> None:
    """Reload saved data, without losing unsaved State if storage is blocked."""
    if read_saved_data() is None:
        return
    latest = load_profiles()
    state.profiles = latest.profiles
    state.current_profile = latest.current_profile


def get_profile(state: State, profile_id: str) -> Profile | None:
    """Find a profile by its unique identifier."""
    for profile in state.profiles:
        if profile.profile_id == profile_id:
            return profile
    return None


def match_reasons(first: Profile, second: Profile) -> list[str]:
    """Return labels for the preferences two students share."""
    reasons = []
    if first.sleep == second.sleep:
        reasons.append("Same sleep schedule")
    if first.cleanliness == second.cleanliness:
        reasons.append("Same cleanliness")
    if first.noise == second.noise:
        reasons.append("Same noise level")
    if first.looking_for == second.looking_for:
        reasons.append("Same goal")
    if first.guests == second.guests:
        reasons.append("Same guest preference")
    if first.smoking == second.smoking:
        if first.smoking == "No":
            reasons.append("Both non-smokers")
        else:
            reasons.append("Same smoking preference")
    return reasons


def compatibility(first: Profile, second: Profile) -> int:
    """Six equal-weight answers produce a percentage from 0 to 100."""
    return round(len(match_reasons(first, second)) / 6 * 100)


def find_matches(user: Profile, profiles: list[Profile]) -> list[Profile]:
    """Sort all OTHER students by compatibility, highest score first."""
    matches = []
    for profile in profiles:
        if profile.profile_id != user.profile_id:
            matches.append(profile)
    # The lambda gives sorted() each candidate's compatibility score.
    # reverse=True places the highest scores first.
    return sorted(matches, key=lambda person: compatibility(user, person), reverse=True)


# Site-wide styling, written with Drafter's built-in CSS support.
set_website_title("Campus Roomfit")
set_site_information(
    author="Josh",
    description="A student roommate and study-partner compatibility matcher.",
    sources="Drafter documentation and AI-assisted development.",
    planning="See the brainstorming and design worksheets in the repository.",
    links=[],
)
set_website_framed(False)
hide_debug_information()
set_website_style("none")
add_website_css("body", "margin:0; background:#f7f8f7; color:#1c2925; font-family:Arial,Helvetica,sans-serif;")
add_website_css(".app-shell", "max-width:850px; margin:48px auto; padding:0 20px 60px;")
add_website_css(".site-nav",
    'display:flex; gap:14px; align-items:center; justify-content:space-between; '
    'flex-wrap:wrap; padding:12px 18px; background:white; border:1px solid #e6ebe8; '
    'border-radius:12px;'
)
add_website_css(".brand", "font-weight:800; font-size:19px; color:#216f5b;")
add_website_css(".nav-links", "display:flex; flex-wrap:wrap; gap:8px;")
add_website_css(".nav-links button",
    'background:transparent; border:none; box-shadow:none; color:#2d6658; '
    'font-size:13px; padding:7px 9px; cursor:pointer;'
)
add_website_css(".nav-links button:hover", "background:#e8f3ee; border-radius:8px;")
add_website_css(".page-content", "max-width:620px; margin:46px auto 0;")
add_website_css(".page-title", "font-size:31px; line-height:1.18; font-weight:800; margin:0 0 12px;")
add_website_css(".page-description", "color:#5e6c66; font-size:15px; line-height:1.6; margin-bottom:25px;")
add_website_css(".form-card",
    'background:#fff; padding:26px; border:1px solid #e0e7e3; border-radius:13px; '
    'box-shadow:0 2px 9px rgba(10,40,28,.025);'
)
add_website_css(".field", "display:flex; flex-direction:column; gap:8px; margin-bottom:20px; flex:1; min-width:180px;")
add_website_css(".field-label", "font-weight:700; font-size:13px; color:#273731;")
add_website_css(".field input:not([type=checkbox]),.field select,.field textarea",
    'width:100%; box-sizing:border-box; border:1px solid #abbab2; border-radius:7px; '
    'padding:11px 12px; font:inherit; background:#fff; color:#25342d;'
)
add_website_css(".field textarea", "min-height:95px; resize:vertical;")
add_website_css(".form-row", "display:flex; flex-wrap:wrap; column-gap:16px;")
add_website_css(".check-row", "display:flex; gap:25px; flex-wrap:wrap; align-items:center; margin:7px 0 22px;")
add_website_css(".check-item", "display:flex; align-items:center; gap:7px; font-size:13px;")
add_website_css(".primary-action button",
    'background:#216f5b; border:1px solid #216f5b; border-radius:7px; color:white; '
    'padding:12px 20px; font-weight:700; cursor:pointer;'
)
add_website_css(".primary-action button:hover", "background:#165a49;")
add_website_css(".secondary-action button",
    'background:white; color:#216f5b; border:1px solid #216f5b; border-radius:7px; '
    'padding:11px 18px; font-weight:700; cursor:pointer;'
)
add_website_css(".match-card",
    'display:flex; gap:20px; align-items:center; background:white; border:1px solid '
    '#e1e7e3; border-radius:12px; padding:21px; margin:13px 0; box-shadow:0 1px 4px '
    'rgba(10,40,28,.025);'
)
add_website_css(".score-circle",
    'display:flex; justify-content:center; align-items:center; flex-shrink:0; '
    'height:78px; width:78px; border-radius:50%; font-size:19px; font-weight:800; '
    'color:#fff; background:#247b65;'
)
add_website_css(".score-mid", "background:#548c7e;")
add_website_css(".score-low", "background:#82968e;")
add_website_css(".match-detail", "flex:1; min-width:0;")
add_website_css(".match-head",
    'display:flex; align-items:baseline; justify-content:space-between; '
    'flex-wrap:wrap; gap:8px; margin-bottom:7px;'
)
add_website_css(".match-name", "font-size:18px; font-weight:800;")
add_website_css(".match-type", "font-size:12px; color:#53655c;")
add_website_css(".match-bio", "font-size:13px; line-height:1.45; color:#4b5b53; margin-bottom:10px;")
add_website_css(".match-tags", "display:flex; flex-wrap:wrap; gap:6px;")
add_website_css(".match-tag",
    'display:inline-block; background:#e6f2ed; color:#2b6352; padding:5px 9px; '
    'border-radius:20px; font-size:11px;'
)
add_website_css(".info-card",
    'background:white; border:1px solid #e1e7e3; border-radius:12px; padding:22px; '
    'margin-bottom:14px; line-height:1.65;'
)
add_website_css(".profile-actions", "display:flex; align-items:center; flex-wrap:wrap; gap:10px; margin-top:14px;")
add_website_css(".danger-action button",
    'background:#fff; border:1px solid #b44a4a; color:#a13131; border-radius:7px; '
    'padding:10px 15px; cursor:pointer;'
)
add_website_css(".muted-note", "color:#738179; font-size:12px; margin-top:14px;")
add_website_css("@media (max-width:600px)",
    '.app-shell{margin:14px auto;padding:0 12px 35px;} '
    '.page-content{margin-top:30px;} .form-card{padding:18px;} '
    '.page-title{font-size:26px;} .match-card{padding:15px;gap:13px;} '
    '.score-circle{height:62px;width:62px;font-size:16px;}'
)


def navigation() -> object:
    """Build the navigation buttons shown on every page."""
    return Div(
        Div("Campus Roomfit", classes="brand"),
        Div(
            Button("Home", "index"),
            Button("Create profile", "create_profile"),
            Button("My matches", "results"),
            Button("All profiles", "all_profiles"),
            Button("How scoring works", "about"),
            classes="nav-links",
        ),
        classes="site-nav",
    )


def layout(state: State, *contents) -> Page:
    """Wrap page content in a consistent layout."""
    return Page(state, [Div(navigation(), Div(*contents, classes="page-content"), classes="app-shell")])


def field(label: str, control: object) -> object:
    """Show a labeled form input."""
    return Div(Div(label, classes="field-label"), control, classes="field")


def button(label: str, route_name: str, primary: bool = True) -> object:
    """Show a styled navigation or submit button."""
    return Div(Button(label, route_name), classes="primary-action" if primary else "secondary-action")


def card_for(user: Profile, candidate: Profile) -> object:
    """Show one candidate and its compatibility score."""
    percentage = compatibility(user, candidate)
    score_class = "score-circle"
    if percentage < 50:
        score_class += " score-low"
    elif percentage < 75:
        score_class += " score-mid"
    reasons = match_reasons(user, candidate)
    tags = []
    for reason in reasons:
        tags.append(Div(reason, classes="match-tag"))
    if not tags:
        tags.append(Div("Different preferences", classes="match-tag"))
    return Div(
        Div(str(percentage) + "%", classes=score_class),
        Div(
            Div(Div(candidate.name, classes="match-name"),
                Div(candidate.looking_for, classes="match-type"), classes="match-head"),
            Div(candidate.bio, classes="match-bio"),
            Div(*tags, classes="match-tags"),
            classes="match-detail",
        ),
        classes="match-card",
    )


@route
def index(state: State) -> Page:
    """Show the home page."""
    refresh(state)
    return layout(state,
        Div("Find people who fit your life.", classes="page-title"),
        Div((
            'Meet compatible roommates and study partners based on the way '
            'you live and study — with clear reasons for every match.'
        ), classes="page-description"),
        Div(
            Div("A better match starts with a few simple questions.", classes="match-name"),
            Div((
                'Tell us when you sleep, how you like your space, and what you '
                'are looking for. Your profile joins the saved student list.'
            ), classes="match-bio"),
            button("Create my profile", "create_profile"),
            classes="info-card",
        ),
        Div((
            'Profiles are saved in this browser (or a JSON file when run as'
            ' a desktop program). Example students are fictional.'
        ), classes="muted-note"),
    )


@route
def create_profile(state: State) -> Page:
    """Start a new profile and reset match filtering."""
    refresh(state)
    state.editing_id = ""
    state.match_filter = "Same goal"
    return profile_form(state, None)


def profile_form(state: State, current: Profile | None) -> Page:
    """Build a profile creation or editing form."""
    return layout(state,
        Div("Tell us how you live and study", classes="page-title"),
        Div((
            'Answer a few quick questions and see who fits you best, with '
            'the reasons why.'
        ), classes="page-description"),
        Div(
            field("Name", TextBox("name", current.name if current else "")),
            Div(
                field("Sleep schedule", SelectBox("sleep", ["Early bird", "Night owl"],
                    current.sleep if current else "Early bird")),
                field("Cleanliness level", SelectBox("cleanliness", ["Very tidy", "Moderately tidy",
                    "Relaxed"], current.cleanliness if current else "Very tidy")),
                classes="form-row",
            ),
            Div(
                field("Noise level", SelectBox("noise", ["Quiet", "Some noise"],
                    current.noise if current else "Quiet")),
                field("Looking for", SelectBox("looking_for", ["Roommate", "Study partner"],
                    current.looking_for if current else "Roommate")),
                classes="form-row",
            ),
            Div("Preferences", classes="field-label"),
            Div(
                Div(CheckBox("smoker", current.smoking == "Yes" if current else False), "I smoke",
                    classes="check-item"),
                Div(CheckBox("guests_ok", current.guests == "Yes" if current else True),
                    "Guests are okay", classes="check-item"),
                classes="check-row",
            ),
            field("Short bio", TextArea("bio", current.bio if current else "", rows=3)),
            button("Save profile and find matches", "save_profile"),
            classes="form-card",
        ),
    )


@route
def edit_profile(state: State) -> Page:
    """Open the editing form for the selected profile."""
    refresh(state)
    if state.current_profile is None:
        return create_profile(state)
    state.editing_id = state.current_profile.profile_id
    return profile_form(state, state.current_profile)


@route
def save_profile(state: State, name: str, sleep: str, cleanliness: str,
                 noise: str, looking_for: str, smoker: bool, guests_ok: bool, bio: str) -> Page:
    """Validate and save form answers as a profile."""
    if not name.strip():
        return layout(state,
            Div("Name required", classes="page-title"),
            Div("Please enter your name before saving.", classes="page-description"),
            button("Go back", "create_profile"),
        )
    refresh(state)
    existing = get_profile(state, state.editing_id) if state.editing_id else None
    if existing is None:
        existing = Profile("", "", "", "", "", "", "", "", uuid4().hex)
        state.profiles.append(existing)
    existing.name = name.strip()
    existing.looking_for = looking_for
    existing.sleep = sleep
    existing.cleanliness = cleanliness
    existing.noise = noise
    existing.guests = "Yes" if guests_ok else "No"
    existing.smoking = "Yes" if smoker else "No"
    existing.bio = bio.strip()
    state.current_profile = existing
    state.match_filter = "Same goal"
    state.editing_id = ""
    save_profiles(state)
    return results(state)


@route
def select_profile(state: State, chosen_profile: str) -> Page:
    """Choose the profile used for matching."""
    refresh(state)
    # Dropdown labels contain the unique profile ID, so duplicate names work.
    chosen_id = chosen_profile.split(" | ")[0]
    chosen = get_profile(state, chosen_id)
    if chosen is not None:
        state.current_profile = chosen
        save_profiles(state)
    state.match_filter = "Same goal"
    return results(state)


@route
def confirm_delete(state: State) -> Page:
    """Ask the user to confirm profile deletion."""
    refresh(state)
    if state.current_profile is None:
        return all_profiles(state)
    return layout(state,
        Div("Delete " + state.current_profile.name + "?", classes="page-title"),
        Div((
            'This permanently removes the profile from the saved list and '
            'matching results. This cannot be undone.'
        ), classes="page-description"),
        Div(button("Yes, delete this profile", "delete_profile", False),
            button("Cancel", "results", False), classes="profile-actions"),
    )


@route
def delete_profile(state: State) -> Page:
    """Remove the selected profile from saved profiles."""
    refresh(state)
    if state.current_profile is not None:
        chosen_id = state.current_profile.profile_id
        state.profiles = [p for p in state.profiles if p.profile_id != chosen_id]
        state.current_profile = None
        state.editing_id = ""
        save_profiles(state)
    return all_profiles(state)


@route
def results(state: State) -> Page:
    """Show compatibility-ranked matching results."""
    refresh(state)
    if state.current_profile is None:
        return create_profile(state)
    user = state.current_profile
    matches = find_matches(user, state.profiles)
    if state.match_filter == "Same goal":
        matches = [p for p in matches if p.looking_for == user.looking_for]
    elements = [
        Div("Your top matches, " + user.name, classes="page-title"),
        Div(
            "Looking for a " + user.looking_for.lower() + " · " + user.sleep
            + " · " + user.noise + " · " + user.cleanliness,
            classes="page-description",
        ),
    ]
    elements.append(Div(
        button("Same goal only", "show_same_goal", False),
        button("Show all profiles", "show_all_matches", False),
        classes="profile-actions",
    ))
    if matches:
        for profile in matches:
            elements.append(card_for(user, profile))
    else:
        elements.append(Div("No other student profiles yet.", classes="info-card"))
    elements.append(Div(
        button("Edit my profile", "edit_profile", False),
        button("Create another profile", "create_profile", False),
        button("Delete my profile", "confirm_delete", False),
        classes="profile-actions",
    ))
    elements.append(Div((
        'Scores reflect six equal-weight answers, not a guarantee of '
        'compatibility.'
    ), classes="muted-note"))
    return layout(state, *elements)


@route
def show_same_goal(state: State) -> Page:
    """Limit matching results to students seeking the same type of match."""
    state.match_filter = "Same goal"
    return results(state)


@route
def show_all_matches(state: State) -> Page:
    """Allow matches across roommate and study-partner goals."""
    state.match_filter = "All profiles"
    return results(state)


@route
def all_profiles(state: State) -> Page:
    """Show all saved profiles and the selection control."""
    refresh(state)
    elements = [
        Div("All student profiles", classes="page-title"),
        Div("Saved profiles from this browser. Select one to see its matches or edit it.", classes="page-description"),
    ]
    if state.profiles:
        options = [person.profile_id + " | " + person.name for person in state.profiles]
        default_option = options[0]
        if state.current_profile is not None:
            default_option = state.current_profile.profile_id + " | " + state.current_profile.name
        elements.append(Div(
            field("Choose your profile", SelectBox("chosen_profile", options, default_option)),
            button("Use selected profile", "select_profile"),
            classes="form-card",
        ))
    for person in state.profiles:
        label = person.name
        if state.current_profile and state.current_profile.profile_id == person.profile_id:
            label += " (selected)"
        elements.append(Div(
            Div(label + " · " + person.looking_for, classes="match-name"),
            Div(person.bio, classes="match-bio"),
            Div(person.sleep + " · " + person.cleanliness + " · " + person.noise, classes="muted-note"),
            classes="info-card",
        ))
    if not state.profiles:
        elements.append(Div("No profiles saved yet.", classes="info-card"))
    elements.append(button("Add a new profile", "create_profile"))
    return layout(state, *elements)


@route
def about(state: State) -> Page:
    """Explain the matching score."""
    refresh(state)
    return layout(state,
        Div("How scoring works", classes="page-title"),
        Div("A simple, transparent way to compare student habits.", classes="page-description"),
        Div(
            Div("We compare six preferences:", classes="match-name"),
            BulletedList(["Sleep schedule", "Cleanliness", "Noise level",
                "Roommate or study-partner goal", "Guests", "Smoking"]),
            Div((
                'Each answer that matches earns 1 point. The score is (matching'
                ' answers ÷ 6) × 100, rounded to a whole percentage.'
            ), classes="match-bio"),
            Div((
                'Highest-scoring students appear first. You can choose whether '
                'to include students with different goals.'
            ), classes="match-bio"),
            classes="info-card",
        ),
        button("Find my matches", "create_profile"),
    )


if __name__ == "__main__":
    start_server(load_profiles())
