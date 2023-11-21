var urlAtual = window.location.href;
        var code;
        let numbers = [];
        let rdm = 1;
        let scraText
        let driText 
        
        function fetchs(url, id, veri) {
            fetch((urlAtual+ '/' + url), {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
                body: JSON.stringify({}),
            })
            
            .then(response => response.json())
            
            .then(data => {
                console.log(data.message);
                let driver = document.getElementById(id);
                driver.innerHTML = data.message;
                if (veri === true) {
                    code = data.code;
                    if ((code in numbers) === false){
                        if (code != 'null'){
                            console.log(code);
                            numbers.push(code);
                        };
                    };
                    
                };
            })
            
            .catch(error => {
                console.log('Deu um error: ' + error)
            });
        }; 
    
        const driver = async () => {
            await fetchs('driver', 'driver-value', false);
        }
        driver()
        
        setInterval(() => {
            driText = document.getElementById('driver-value').innerHTML;
            scraText = document.getElementById('scrape-value').innerHTML;
        }, 1000);

        setInterval(async () => {
            if (scraText === 'Sms Encontrado!!!'){
                await fetchs('task', 'code', false);
                rdm = 1
            }
        }, 1000);
    
        setInterval(() => {
            if (scraText === 'Novo número encontrado!!!'){
                if (rdm > 0){
                    fetchs('task3', 'driver-value', false);
                    rmd = 0
                }
            }
        }, 1000);

        setInterval(() => {
            if (scraText === 'Não há números novos...' || scraText === 'Carregando...') {
                fetchs('scrape', 'scrape-value', true);
            }
        }, 1000);  
    
        setInterval(() => {
            if (scraText === 'Novo número encontrado!!!' || scraText === 'Nenhum sms encontrado...') {
                fetchs('/task2', 'scrape-value', true);
            }
        }, 1000)
