const form = document.getElementById("register-form");
const msg = document.getElementById("msg");

function setMsg(type, text){
  msg.className = '';
  msg.textContent = text;
  if (type === 'error') {
    msg.classList.add('error');
  } else if (type === 'success') {
    msg.classList.add('success');
  } else {
    msg.classList.add('status');
  }
  msg.style.display = 'block';
}

function clearMsg(){
  msg.style.display = 'none';
  msg.className = '';
  msg.textContent = '';
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  clearMsg();
  setMsg('status','Registering...');

  const payload = {
    username: form.username.value.trim(),
    email: form.email.value.trim(),
    password: form.password.value
  };

  try {
    const res = await fetch("/api/users", {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify(payload)
    });

    const body = await (async ()=>{ try { return await res.json(); } catch { return null; } })();

    if (res.ok) {
      setMsg('success','Registration successful! Redirecting…');
      setTimeout(()=> { location.href = '/'; }, 700);
      return;
    }

    setMsg('error', body?.detail || 'Registration failed. Please try again.');
  } catch (err) {
    console.error(err);
    setMsg('error','Network error. Try again.');
  }
});