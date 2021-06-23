



router.get("/", (req, res) => {
    User.find()
        .sort({ id: -1 })
        .then((users) => res.json(users));
});

// router.post("/", (req, res) => {
//     console.log(req)
//   const newUser = new User({
//     firstname: req.body.firstname,
//     lastname: req.body.lastname,

//     email: req.body.email,
//     password: req.body.password,
//   });
//   newUser.save().then((user) => res.json(user));
// });


router.get("/cook", (req, res) => {
    const cookies = req.cookies['logged'];
    console.log(cookies)
    res.json(cookies);
});

router.post("/", (req, res) => {
    // Form validation
    // console.log(req)

    const { errors, isValid } = validateRegisterInput(req.body);

    // console.log("ERRRRRRRRRRRRR")
    // console.log(errors)
    // Check validation
    if (!isValid) {
        return res.status(400).json(errors);
    }
    User.findOne({ email: req.body.email }).then(user => {
        if (user) {
            return res.status(400).json({ email: "Email already exists" });
        } else {

            const saltRounds = 10;

            bcrypt.hash(req.body.password, saltRounds, function (err, hash) {

                const newUser = new User({
                    firstname: req.body.firstname,
                    lastname: req.body.lastname,
                    email: req.body.email,
                    password: hash
                });
                newUser
                    .save()
                    .then(user => res.json(user))
                    .catch(err => res.send(err));

            });


            // const salt  =  10;
            // const pass = req.body.password;
            // const f = bcrypt.hash(pass, salt);
            // console.log(f);
            // console.log("PASSSS")
            // console.log(pass);
            // const newUser = new User({
            //     firstname: req.body.firstname,
            //     lastname: req.body.lastname,
            //     email: req.body.email,
            //     password: f
            // });
            // bcrypt.genSalt(10, (err, salt) => {
            // 	bcrypt.hash(newUser.password, salt, (err, hash) => {
            // 		if (err) throw err;
            // 		newUser.password = hash;
            // 		newUser
            // 			.save()
            // 			.then(user => res.json(user))
            // 			.catch(err => res.send(err));
            // 	});
            // });
            // Hash password before saving in database
            // newUser
            // 	.save()
            // 	.then(user => res.json(user))
            // 	.catch(err => res.send(err));
        }
    });
});


router.post("/login", (req, res) => {
    // Form validation
    const { errors, isValid } = validateLoginInput(req.body);
    // Check validation
    if (!isValid) {
        // res.cookie('logged',false,{domain:''});
        res.cookie('logged', false);

        res.status(400).json(errors);
        return res;
    }
    const email = req.body.email;
    const password = req.body.password;
    // Find user by email
    User.findOne({ email }).then(user => {
        const p1 = user.password;
        // Check if user exists
        if (!user) {
            res.cookie('logged', false);
            // res.cookie('logged',false,{domain:''});

            res.status(404).json({
                error: "Email not found",
                emailnotfound: "Email not found"
            });
            return res;
        }

        bcrypt.compare(password, p1, function (err, res1) {
            if (err) {
                // handle error
                console.log("RERROR")
                res.cookie('logged', false, { domain: '' });

                //   res.cookie('logged',false);

                res.status(400).json({
                    error: "Password Incorrect",
                    passwordincorrect: "Password incorrect"
                });
                return res;
            }
            else if (!res1) {
                // res.cookie('logged',false);
                res.cookie('logged', false, { domain: '' });


                res.status(400).json({
                    error: "Password Incorrect",
                    passwordincorrect: "Password incorrect"
                });
                return res;

            }
            else {
                // res.cookie('logged',true);
                res.cookie('logged', true, { domain: '' });

                res.json({
                    success: true,
                    user: user
                });
                return res;
                // Send JWT
            }
        });
        // if(bcrypt.compare(password, p1))
        // 	{
        // 	// res.setHeader('Set-cookie','loggedIn = false')
        // 	res.cookie('logged',false);

        //     res.status(400).json({
        //         error: "Password Incorrect",
        //         passwordincorrect: "Password incorrect"
        //     });
        // 	return res;
        // }
        // else
        {
            // res.setHeader('Set-cookie','loggedIn = true')
            // res.cookie('logged',true);


            //  res.json({
            //     					success: true,
            //     					user: user
            //     				});
            // 					return res;
        }
        // Check password
        // bcrypt.compare(password, user.password).then(isMatch => {
        // 	if (isMatch) {
        // 		// User matched
        // 		// Create JWT Payload
        // 		const payload = {
        // 			id: user.id,
        // 			name: user.name
        // 		};
        // 		// Sign token
        // 		jwt.sign(
        // 			payload,
        // 			keys.secretOrKey,
        // 			{
        // 				expiresIn: 31556926 // 1 year in seconds
        // 			},
        // 			(err, token) => {
        // 				res.json({
        // 					success: true,
        // 					token: "Bearer " + token,
        // 					user: user
        // 				});
        // 			}
        // 		);
        // 	} else {
        // 		return res.status(400).json({
        // 			error: "Password Incorrect",
        // 			passwordincorrect: "Password incorrect"
        // 		});
        // 	}
        // });
    });
});



// router.delete("/:id", (req, res) => {
//   Factory.findById(req.params.id)
//     .then((factory) => factory.remove().then(() => res.json({ success: true })))
//     // .catch((err) => res.statur(404).json({ success: false }));
// });

module.exports = router;
