let rulesArray = [];
        async function createRules() {
            const rulesInput = document.getElementById("rule-input").value.trim();
            const rules = rulesInput.split('\n').filter(rule => rule.trim());

            if (rules.length === 0) {
                document.getElementById("create-message").innerText = "Please enter valid rules.";
                return;
            }

            try {
                const createPromises = rules.map(rule => fetch("http://127.0.0.1:5000/rules", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ rule: rule.trim() })
                }));

                const responses = await Promise.all(createPromises);

                if (responses.some(response => !response.ok)) {
                    throw new Error("Some rules failed to create.");
                }

                rulesArray.push(...rules);
                document.getElementById("create-message").innerText = "All rules created successfully!";
                document.getElementById("rule-input").value = "";
            } catch (error) {
                console.error(error);
                document.getElementById("create-message").innerText = "Failed to create rules.";
            }
        }

        function displayRules() {
            const rulesDiv = document.getElementById("rules-list-content");
            rulesDiv.innerHTML = rulesArray.length
                ? rulesArray.map((rule, i) => `<p class="rule-item">Rule ${i + 1}: ${rule}</p>`).join("")
                : "No rules available.";
        }

        async function combineRules() {
            try {
                const response = await fetch("http://127.0.0.1:5000/combine", { method: "POST" });
                const data = await response.json();
                alert("Combined Rule:\n" + JSON.stringify(data.combined_rule, null, 2));
            } catch (error) {
                alert("Failed to combine rules.");
            }
        }

        async function evaluateRule() {
            const dataInput = document.getElementById("data-input").value.trim();
            try {
                const response = await fetch("http://127.0.0.1:5000/evaluate", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ data: JSON.parse(dataInput) })
                });

                const result = await response.json();
                document.getElementById("evaluate-result").innerText = "Result: " + JSON.stringify(result.result);
            } catch (error) {
                document.getElementById("evaluate-result").innerText = "Invalid input or error.";
            }
        }

        async function modifyRule() {
            const index = parseInt(document.getElementById("modify-index").value);
            const type = document.getElementById("modify-type").value;
            const newValue = document.getElementById("modify-value").value;

            try {
                const response = await fetch("http://127.0.0.1:5000/modify_rule", {
                    method: "PUT",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ index, type, new_value: newValue })
                });

                const data = await response.json();
                document.getElementById("modify-message").innerText = data.message;
                displayRules();
            } catch (error) {
                document.getElementById("modify-message").innerText = "Modification failed.";
            }
        }
        document.getElementById("showRules").addEventListener("click", displayRules);