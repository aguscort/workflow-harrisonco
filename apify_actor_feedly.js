const Apify = require('apify');
Apify.main(async () => {
    const input = await Apify.getValue('INPUT');
    console.log('Launching Puppeteer...');
    const browser = await Apify.launchPuppeteer();

    var xpath_expr_btnlgn = '//*[@id="feedlyPageFX"]/div/header/div/button';
    var xpath_expr_btnlgnmtd = '/html/body/div/a[2]';
    var xpath_expr_user = '/html/body/div/form/input[1]';
    var xpath_expr_pass = '/html/body/div/form/input[2]';
    var xpath_expr_btngo = '/html/body/div/form/input[4]'; 
    // fs    
    var xpath_expr_addfedd = '//*[@id="feedlyChrome__leftnav-dock-wrapper"]/div/div[2]/button[1]/i';
    var xpath_expr_google =  '//*[@id="feedlyPageFX"]/div/div[1]/a[2]';
    var xpath_expr_search_bar = '//*[@id="feedlyPageFX"]/div/div[2]/div/div[1]/div/div/div/input';
    var xpath_expr_follow =  '//*[@id="feedlyPageFX"]/div/div[2]/div/div[2]/div/div[2]/div[1]/div[2]/div/div[1]/button';
    var xpath_expr_search_group = '//*[@id="feedlyPageFX"]/div/div[2]/div/div[2]/div/div[2]/div[1]/div[2]/div/div[1]/div/div[1]/div/div/input';
    var xpath_expr_addgroup  = '//*[@id="feedlyPageFX"]/div/div[2]/div/div[2]/div/div[2]/div[1]/div[2]/div/div[1]/div/div[1]/menu/li/span';
    // fs
    var xpath_expr_account =   '//*[@id="feedlyChrome__leftnav-dock-wrapper"]/div/div[3]/div/div';
    var xpath_expr_logout = '//*[@id="feedlyChrome__leftnav-dock-wrapper"]/div/div[3]/div/div[2]/div[1]/menu/li[9]';
    
    console.log('Sign in ...');
    console.log(input);
    const page = await browser.newPage();
    await page.goto('https://feedly.com/i/welcome');

    // Log in Owler
    try {     
        await new Promise(r => setTimeout(r, 3000));
        await page.waitForXPath(xpath_expr_btnlgn);    
        const btnlgn = await page.$x(xpath_expr_btnlgn);
        await btnlgn[0].click();
        await new Promise(r => setTimeout(r, 3000));
        await page.waitForXPath(xpath_expr_btnlgnmtd);    
        const btnmethod = await page.$x(xpath_expr_btnlgnmtd);
        await btnmethod[0].click();
        await new Promise(r => setTimeout(r, 3000));
        const user = await page.$x(xpath_expr_user);
        await user[0].type(input.user);
        const passwd = await page.$x(xpath_expr_pass);
        await passwd[0].type(input.passwd);
        await page.waitForXPath(xpath_expr_btngo);    
        const btngo = await page.$x(xpath_expr_btngo);
        await btngo[0].click();        
        // Search Company
        await new Promise(r => setTimeout(r, 3000));
        await page.waitForXPath(xpath_expr_addfedd);    
        const addfeed = await page.$x(xpath_expr_addfedd);
        await addfeed[0].click();
        await page.waitForXPath(xpath_expr_google);
        const feedmethod = await page.$x(xpath_expr_google);
        await feedmethod[0].click();
        await page.waitForXPath(xpath_expr_search_bar);
        const srch_bar = await page.$x(xpath_expr_search_bar);
        await srch_bar[0].type('"' +  input.company + '"'); 
        await page.waitForXPath(xpath_expr_follow);    
        const btnfollow = await page.$x(xpath_expr_follow);
        let value = await page.evaluate(el => el.textContent, btnfollow[0])
        console.log(value);        
        if (((input.action == "add") && (value == "Follow")) || ((input.action == "remove") && (value == "Following"))) {                    
            await btnfollow[0].click();        
            await page.waitForXPath(xpath_expr_search_group);
            const srch_feed = await page.$x(xpath_expr_search_group);
            await srch_feed[0].type('Harrison Co'); 
            await page.waitForXPath(xpath_expr_addgroup);    
            const btnadd = await page.$x(xpath_expr_addgroup); 
            await btnadd[0].click(); 
            console.log('Action performedd...');
            console.log('Saving screenshot...');
            const screenshotBuffer = await page.screenshot();
            await Apify.setValue('screenshot.png', screenshotBuffer, { contentType: 'image/png' });                    
            await Apify.pushData([{ 'company_url': input.company },
                { "action" : input.action }]);              
        } else {
            //console.log('Saving screenshot...');
            //const screenshotBuffer = await page.screenshot();
            //await Apify.setValue('screenshot.png', screenshotBuffer, { contentType: 'image/png' });                    
            await Apify.pushData([{ 'company_url': input.company },
                { "action" : "Nothing happens" }]);              
        }
        await new Promise(r => setTimeout(r, 2000));
        await page.waitForXPath(xpath_expr_account);
        const account = await page.$x(xpath_expr_account);
        await account[0].click();
        const logout = await page.$x(xpath_expr_logout);
        await logout[0].click();         
    }
    catch (err) {
        console.log('Nothing done.');
    }
    //console.log('You can check the output in the key-value on the following URLs:');
    //const storeId = process.env.APIFY_DEFAULT_KEY_VALUE_STORE_ID;
    //console.log(`- https://api.apify.com/v2/key-value-stores/${storeId}/records/screenshot.png`)
    await new Promise(resolve => setTimeout(resolve, 3000));
    console.log('Closing Puppeteer...');
    await browser.close();
});