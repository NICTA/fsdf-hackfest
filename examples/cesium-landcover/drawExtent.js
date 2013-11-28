   function drawExtent(scene, ellipsoid, myHandler) {
        
        var DrawExtentHelper = function(scene, handler) {
            this._canvas = scene.getCanvas();
            this._scene = scene;
            this._ellipsoid = scene.getPrimitives().getCentralBody().getEllipsoid();
            this._finishHandler = handler;
            this._mouseHandler = new Cesium.ScreenSpaceEventHandler(this._canvas);
            this._extentPrimitive = new Cesium.ExtentPrimitive();
            this._extentPrimitive.asynchronous = false;
            this._scene.getPrimitives().add(this._extentPrimitive);
        };
        
        DrawExtentHelper.prototype.enableInput = function() {
            var controller = this._scene.getScreenSpaceCameraController();
            
            controller.enableTranslate = true;
            controller.enableZoom = true;
            controller.enableRotate = true;
            controller.enableTilt = true;
            controller.enableLook = true;
        };
        
        DrawExtentHelper.prototype.disableInput = function() {
            var controller = this._scene.getScreenSpaceCameraController();
            
            controller.enableTranslate = false;
            controller.enableZoom = false;
            controller.enableRotate = false;
            controller.enableTilt = false;
            controller.enableLook = false;
        };
        
        DrawExtentHelper.prototype.getExtent = function(mn, mx) {
            var e = new Cesium.Extent();

            // Re-order so west < east and south < north
            e.west = Math.min(mn.longitude, mx.longitude);
            e.east = Math.max(mn.longitude, mx.longitude);
            e.south = Math.min(mn.latitude, mx.latitude);
            e.north = Math.max(mn.latitude, mx.latitude);

            // Check for approx equal (shouldn't require abs due to re-order)
            var epsilon = Cesium.Math.EPSILON7;

            if ((e.east - e.west) < epsilon) {
                e.east += epsilon * 2.0;
            }

            if ((e.north - e.south) < epsilon) {
                e.north += epsilon * 2.0;
            }

            return e;
        };
        
        DrawExtentHelper.prototype.setPolyPts = function(mn, mx) {
            this._extentPrimitive.extent = this.getExtent(mn, mx);
        };
        
        DrawExtentHelper.prototype.setToDegrees = function(w, s, e, n) {
            var toRad = Cesium.Math.toRadians;
            var mn = new Cesium.Cartographic(toRad(w), toRad(s));
            var mx = new Cesium.Cartographic(toRad(e), toRad(n));
            this.setPolyPts(mn, mx);
        };
        
        DrawExtentHelper.prototype.handleRegionStop = function(movement) {
            this.enableInput();
            var cartesian = this._scene.getCamera().controller.pickEllipsoid(movement.position,
                    this._ellipsoid);
            if (cartesian) {
                this._click2 = this._ellipsoid.cartesianToCartographic(cartesian);
            }
            this._mouseHandler.destroy();

            this._finishHandler(this.getExtent(this._click1, this._click2));
        };
        
        DrawExtentHelper.prototype.handleRegionInter = function(movement) {
            var cartesian = this._scene.getCamera().controller.pickEllipsoid(movement.endPosition,
                    this._ellipsoid);
            if (cartesian) {
                var cartographic = this._ellipsoid.cartesianToCartographic(cartesian);
                this.setPolyPts(this._click1, cartographic);
            }
        };
        
        DrawExtentHelper.prototype.handleRegionStart = function(movement) {
            var cartesian = this._scene.getCamera().controller.pickEllipsoid(movement.position,
                    this._ellipsoid);
            if (cartesian) {
                var that = this;
                this._click1 = this._ellipsoid.cartesianToCartographic(cartesian);
                this._mouseHandler.setInputAction(function(movement) {
                    that.handleRegionStop(movement);
                }, Cesium.ScreenSpaceEventType.LEFT_UP);
                this._mouseHandler.setInputAction(function(movement) {
                    that.handleRegionInter(movement);
                }, Cesium.ScreenSpaceEventType.MOUSE_MOVE);
            }
        };
        
        DrawExtentHelper.prototype.start = function() {
            this.disableInput();

            var that = this;

            // Now wait for start
            this._mouseHandler.setInputAction(function(movement) {
                that.handleRegionStart(movement);
            }, Cesium.ScreenSpaceEventType.LEFT_DOWN);
        };
        
        var drawExtentHelper = new DrawExtentHelper(scene, myHandler);
        drawExtentHelper.start();
    }

