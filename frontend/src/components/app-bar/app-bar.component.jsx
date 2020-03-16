import React from 'react'
import './app-bar.styles.css'
import {AppBar, Drawer, IconButton, InputBase, Menu, MenuItem, Toolbar, Typography} from "@material-ui/core";
import SearchIcon from '@material-ui/icons/Search'
import MenuIcon from '@material-ui/icons/Menu';
import ChevronLeftIcon from '@material-ui/icons/ChevronLeft';
import ChevronRightIcon from '@material-ui/icons/ChevronRight';
import NotificationsIcon from '@material-ui/icons/Notifications';
import {fade, makeStyles, useTheme} from '@material-ui/core/styles';
import AccountCircle from '@material-ui/icons/AccountCircle';
import Button from "@material-ui/core/Button";
import {Link} from "react-router-dom";

const useStyles = makeStyles(theme => ({
    root: {
        flexGrow: 1,
    },
    menuButton: {
        marginRight: theme.spacing(2),
    },
    title: {
        flexGrow: 1,
        display: 'none',
        [theme.breakpoints.up('sm')]: {
            display: 'block',
        },
    },
    search: {
        position: 'relative',
        borderRadius: theme.shape.borderRadius,
        backgroundColor: fade(theme.palette.common.white, 0.15),
        '&:hover': {
            backgroundColor: fade(theme.palette.common.white, 0.25),
        },
        marginLeft: 0,
        width: '100%',
        [theme.breakpoints.up('sm')]: {
            marginLeft: theme.spacing(1),
            width: 'auto',
        },
    },
    searchIcon: {
        width: theme.spacing(7),
        height: '100%',
        position: 'absolute',
        pointerEvents: 'none',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
    },
    inputRoot: {
        color: 'inherit',
    },
    inputInput: {
        padding: theme.spacing(1, 1, 1, 7),
        transition: theme.transitions.create('width'),
        width: '100%',
        [theme.breakpoints.up('sm')]: {
            width: 120,
            '&:focus': {
                width: 200,
            },
        },
    },
}));


const AppBarComponent = (props) => {
    const classes = useStyles();
    const theme = useTheme();
    const [open, setOpen] = React.useState(false);
    const [anchorEl, setAnchorEl] = React.useState(null);


    const handleDrawerOpen = () => {
        setOpen(true);
    };

    const handleDrawerClose = () => {
        setOpen(false);
    };

    const handleClick = event => {
        setAnchorEl(event.currentTarget);
    };

    const handleClose = () => {
        setAnchorEl(null);
    };

    const logOut = () => {
        setAnchorEl(null);
    }

    const showAppBar1 = () =>
        (
            <div>
                <IconButton
                    edge="start"
                    className={classes.menuButton}
                    color="inherit"
                    aria-label="open drawer"
                    onClick={handleDrawerOpen}
                >
                    <MenuIcon/>
                </IconButton>
            </div>
        )


    ;

    const showAppBar2 = () => (

        <div className={classes.search}>
            <div className={classes.searchIcon}>
                <SearchIcon/>
            </div>
            <InputBase
                placeholder="Search…"
                classes={{
                    root: classes.inputRoot,
                    input: classes.inputInput,
                }}
                inputProps={{'aria-label': 'search'}}
            />

        </div>

    )
    const showAppBar3 = () => (
        <div>

            <IconButton aria-label="show 17 new notifications" color="inherit">
                <NotificationsIcon/>
            </IconButton>
            <IconButton
                edge="end"
                aria-label="account of current user"
                aria-haspopup="true"
                color="inherit"
                onClick={handleClick}
            >
                <AccountCircle/>
            </IconButton>
        </div>
    )

    return (
        <div>
            <AppBar id={"appBar"} position="static">
                <Toolbar>
                    {showAppBar1()}
                    <Typography className={classes.title} variant="h6" noWrap>
                        Video Processing Application
                    </Typography>
                    <Link to={`/doc`


                    }
                          style={{textDecoration: 'none'}}
                    >
                        <Button variant="contained" color="primary" disableElevation>API DOCUMENTATION</Button>
                    </Link>
                    {showAppBar3()}
                </Toolbar>
            </AppBar>
            <Menu
                id="simple-menu"
                anchorEl={anchorEl}
                keepMounted
                open={Boolean(anchorEl)}
                onClose={handleClose}
            >
                <MenuItem onClick={handleClose}>Profile</MenuItem>
                <MenuItem onClick={handleClose}>My account</MenuItem>
                <MenuItem onClick={logOut}>Logout</MenuItem>
            </Menu>
            <Drawer
                className={classes.drawer}
                variant="persistent"
                anchor="left"
                open={open}
                classes={{
                    paper: classes.drawerPaper,
                }}
            >
                <div className={classes.drawerHeader}>
                    <IconButton onClick={handleDrawerClose}>
                        {theme.direction === 'ltr' ? <ChevronLeftIcon/> : <ChevronRightIcon/>}
                    </IconButton>
                </div>

                <Link to={'/'}
                      style={{textDecoration: 'none'}}
                >
                    <Button onClick={handleDrawerClose}>
                        Home
                    </Button>
                </Link>

            </Drawer>
        </div>
    )
};
export default AppBarComponent