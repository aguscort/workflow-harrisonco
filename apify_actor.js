const Apify = require('apify');
Apify.main(async () => {
    const input = await Apify.getValue('INPUT');
    console.log('Launching Puppeteer...');
    const browser = await Apify.launchPuppeteer();

    var xpath_expr_user = '/html/body/div[2]/div/div[2]/div/div[2]/div/input' 
    var xpath_expr_btn1 = '/html/body/div[2]/div/div[2]/div/div[2]/button[1]' 
    var xpath_expr_pass = '//*[@id="password"]'
    var xpath_expr_btn2 = '/html/body/div[2]/div/div[2]/div/div[2]/button[1]'
    var xpath_expr_search_bar = '//*[@id="header"]/div[1]/div[1]/div/div/input'
    // fs
    var xpath_expr_account =   '//*[@id="root"]/div/div/div[1]/div/div'
    var xpath_expr_logout = '//*[@id="root"]/div/div/div[1]/nav/div[4]/div/button'
    var xpath_expr_account_2 =   '//*[@id="__next"]/div/div[1]/div/div'
    var xpath_expr_logout_2 = '//*[@id="__next"]/div/div[1]/nav/div[4]/div/button'
    // sdf
    var xpath_expr_first_match = '//*[@id="header"]/div[1]/div[1]/div/div[2]/ul/div'
    var xpath_expr_follow_btn = '//*[@id="__next"]/div/div[2]/div/div/div[2]/div/div/div/div[2]/div[1]/div[2]/button'
    var xpath_expr_follow_btn2 = '//*[@id="__next"]/div/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/button'
    var xpath_expr_follow_btn_text = '//*[@id="__next"]/div/div[2]/div/div/div[2]/div/div/div/div[2]/div[1]/div[2]/button/div[2]'                                     
    var xpath_expr_follow_btn_text2 = '//*[@id="__next"]/div/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/button/div[2]'

    console.log('Sign in ...');
    console.log(input);
    const page = await browser.newPage();
    await page.goto('https://www.owler.com/login');

    // Log in Owler 
    await page.waitForXPath(xpath_expr_user);    
    const user = await page.$x(xpath_expr_user);
    await user[0].type(input.user);
    const btn1= await page.$x(xpath_expr_btn1);
    await btn1[0].click();
    await page.waitForXPath(xpath_expr_pass);
    const passwd = await page.$x(xpath_expr_pass);
    await passwd[0].type(input.passwd);
    await page.waitForXPath(xpath_expr_btn2);
    const btn2 = await page.$x(xpath_expr_btn2);
    await btn2[0].click();
    // Search Company
    await new Promise(r => setTimeout(r, 3000));
    await page.waitForXPath(xpath_expr_search_bar);
    const srch_bar = await page.$x(xpath_expr_search_bar);
    await srch_bar[0].type(input.company_url);       
    try {
        // Choose the first option
        await page.waitForXPath(xpath_expr_first_match);
        const match = await page.$x(xpath_expr_first_match);
        await match[0].click();            
        try {
            // Situation 1
            await new Promise(r => setTimeout(r, 3000));
            const company_owler_url = page.url();
            console.log(company_owler_url);                    
            const follow_btn_text = await page.$x(xpath_expr_follow_btn_text);
            let value = await page.evaluate(el => el.textContent, follow_btn_text[0])
            console.log(value); 
            if (((input.action == "add") && (value == "Follow")) || ((input.action == "remove") && (value == "Following"))) {
                await page.waitForXPath(xpath_expr_follow_btn);
                const follow_btn = await page.$x(xpath_expr_follow_btn);
                await follow_btn[0].click();                        
            }
            console.log('Logout with a match ...');
            await Apify.pushData([{ 'company_url': input.company_url },
                { "company_owler_url" : company_owler_url },
                { "action" : input.action }]);
            //Perform logout            
            await page.waitForXPath(xpath_expr_account_2);
            const account_2 = await page.$x(xpath_expr_account_2);
            await account_2[0].click();
            const logout_2 = await page.$x(xpath_expr_logout_2);
            await logout_2[0].click();                
        }        
        catch (err) {
            // Situation 2
            await new Promise(r => setTimeout(r, 3000));
            const company_owler_url = page.url();
            console.log(company_owler_url);                        

            const follow_btn2_text = await page.$x(xpath_expr_follow_btn_text2);
            let value = await page.evaluate(el => el.textContent, follow_btn2_text[0]);
                console.log(value);             
            if (((input.action == "add") && (value == "Follow")) || ((input.action == "remove") && (value == "Following"))) {
                await page.waitForXPath(xpath_expr_follow_btn2);
                const follow_btn2 = await page.$x(xpath_expr_follow_btn2);
                await follow_btn2[0].click();
            }  
            console.log('Logout with a match ...');
            await Apify.pushData([{ 'company_url': input.company_url },
                { "company_owler_url" : company_owler_url },
                { "action" : "Nothing happens" }]);         
            //Perform logout            
            await page.waitForXPath(xpath_expr_account_2);
            const account_2 = await page.$x(xpath_expr_account_2);
            await account_2[0].click();
            const logout_2 = await page.$x(xpath_expr_logout_2);
            await logout_2[0].click();                                      
        }        
    }
    catch(err) {
        //Perform logout
        console.log('Logout without any match ...');
        await new Promise(r => setTimeout(r, 2000));
        await page.waitForXPath(xpath_expr_account);
        const account = await page.$x(xpath_expr_account);
        await account[0].click();
        const logout = await page.$x(xpath_expr_logout);
        await logout[0].click();         
        await Apify.pushData([{ 'company_url': input.company_url },
            { "company_owler_url" : "" },
            { "action" : input.action }]);         
    }
    await new Promise(resolve => setTimeout(resolve, 3000));
    console.log('Closing Puppeteer...');
    await browser.close();
});